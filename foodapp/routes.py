import secrets
import os
from PIL import Image
from flask import Flask, render_template, url_for, redirect, flash, request, jsonify
from foodapp.models import User, Recipe, Ingredient
from foodapp import app, bcrypt, db, mail
from foodapp.forms import RegistrationForm, LoginForm, AddRecipe, UpdateProfile, ChangePassword, EmailPassword
from foodapp.utils import searching_by_dish_name, filter, findRecipe, searching_by_dish_name
from flask_login import login_user, logout_user, current_user
from flask_mail import Message


@app.route("/", methods=['GET', 'POST'])
def reg():
    if current_user.is_authenticated :
        return redirect(url_for('home'))
    else :
        form = RegistrationForm()
        if form.validate_on_submit():
            hash_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            usr = User(username=form.username.data, email=form.email.data, password=hash_pwd)
            db.session.add(usr)
            db.session.commit()
            flash('Your account has been created. Please login to continue', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', form=form)

@app.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated :
        flash('Login successfull, Welcome '+User.query.get(current_user.get_id()).username, 'success')
        return redirect(url_for('home'))
    else :
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data) :
                login_user(user, remember=form.remember.data)
                return redirect(url_for('home'))
            else :
                flash('The email or password you have entered is incorrect. Please try again', 'danger')
        return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('Logout successful', 'info')
    return redirect(url_for('login'))

@app.route("/home", methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated :
        if User.query.get(current_user.get_id()).isEmailVerified == True :
            recipes = Recipe.query.all()
            return render_template('home.html', user=User.query.get(current_user.get_id()))
        else :
            return redirect(url_for('emailverify'))
    else :
        return redirect(url_for('login'))

def save_picture(form_picture) :
    ran_hex = secrets.token_hex(8)
    _, f_extension = os.path.splitext(form_picture.filename)
    picture_fn = ran_hex + f_extension
    picture_path = os.path.join(app.root_path, 'static/images/recipe_pics', picture_fn)

    output_size = (500,500)
    i = Image.open(form_picture)
    new_i = i.resize(output_size)
    new_i.save(picture_path)

    return picture_fn

@app.route("/add", methods=['GET', 'POST'])
def add():
    if current_user.is_authenticated :
        if User.query.get(current_user.get_id()).isEmailVerified == True :
            form = AddRecipe()
            theCheckList = []
            if request.method == 'POST':
                theCheckList = request.form.getlist('ingredient')
                print(theCheckList)
            if form.validate_on_submit():
                recipe = Recipe(name=form.recipe_name.data, procedure=form.procedure.data)
                if form.picture.data :
                    picture_file = save_picture(form.picture.data)
                    recipe.image_file = picture_file
                db.session.add(recipe)
                db.session.commit()
                recipe.author = User.query.get(current_user.get_id())
                
                for i in theCheckList:
                    if Ingredient.query.filter_by(name=i).count() == 0 :
                        print("fdsaf")
                        new_ing = Ingredient(name=i)
                        db.session.add(new_ing)
                        db.session.commit()
                        recipe.ingredients.append(new_ing)
                        db.session.commit()

                    else :
                        recipe.ingredients.append(Ingredient.query.filter_by(name=i).first())
                        db.session.commit()
                        

                return redirect(url_for('add'))
            return render_template('add.html', form=form, user=User.query.get(current_user.get_id()))
        else :
            return redirect(url_for('emailverify'))
    else :
        return redirect(url_for('login'))

@app.route("/delete/<id>", methods=['GET', 'POST'])
def delete(id):
    recipe = Recipe.query.get(id)

    if current_user.is_authenticated :
        if recipe.author == User.query.get(current_user.get_id()) :
            if User.query.get(current_user.get_id()).isEmailVerified == True :
                db.session.delete(recipe)
                db.session.commit()
                return redirect(url_for('account'))
            else :
                return redirect(url_for('emailverify'))
        else :
            return "Unauthorized"
    else :
        return redirect(url_for('login'))

@app.route('/ingredientsearch', methods=['POST', 'GET'])
def ingredientsearch() :
    string = request.form['search']
    print(string)
    if len(string) > 0 :
        ans = filter(string)
    else :
        ans = []
    return jsonify({ "result" : ans })

@app.route('/dish', methods=['POST', 'GET'])
def search_by_dish():
    dish = request.form['dish']
    typeOfSearch = request.form['type']
    ing_list = request.form.getlist('info[]')
    print(dish)
    recipe_list = searching_by_dish_name(dish, ing_list, typeOfSearch)

    passing_recipe_list = []
    for recipe in recipe_list :
        sub_rec = {}
        sub_rec['recipe'] = recipe
        if recipe in User.query.get(current_user.get_id()).recipes_liked :
            sub_rec['liked'] = True
        else :
            sub_rec['liked'] = False
        if recipe in User.query.get(current_user.get_id()).recipes_disliked :
            sub_rec['disliked'] = True
        else :
            sub_rec['disliked'] = False
        sub_rec['likes'] = len(recipe.users_liked)
        sub_rec['dislikes'] = len(recipe.users_disliked)
        print(sub_rec['recipe'].name + ": " + str(sub_rec['disliked']))
        passing_recipe_list.append(sub_rec)
    
    return jsonify({'result' : render_template('recipelist.html', recipes=passing_recipe_list)})

@app.route('/recipe', methods=['POST', 'GET'])
def recipeFiltering() :
    if current_user.is_authenticated :
        if User.query.get(current_user.get_id()).isEmailVerified == True :
            recipes = Recipe.query.all()
            return render_template('recipe.html')
        else :
            return redirect(url_for('emailverify'))
    else :
        return redirect(url_for('login'))

@app.route('/filter', methods=['POST', 'GET'])
def filteredrecipe() :
    ing_list = request.form.getlist('info[]')
    typeOfSearch = str(request.form['type'])
    recipeSearch = request.form['dish']
    recipe_list = searching_by_dish_name(recipeSearch, ing_list, typeOfSearch)

    passing_recipe_list = []
    for recipe in recipe_list :
        sub_rec = {}
        sub_rec['recipe'] = recipe
        if recipe in User.query.get(current_user.get_id()).recipes_liked :
            sub_rec['liked'] = True
        else :
            sub_rec['liked'] = False
        if recipe in User.query.get(current_user.get_id()).recipes_disliked :
            sub_rec['disliked'] = True
        else :
            sub_rec['disliked'] = False
        sub_rec['likes'] = len(recipe.users_liked)
        sub_rec['dislikes'] = len(recipe.users_disliked)
        print(sub_rec['recipe'].name + ": " + str(sub_rec['disliked']))
        passing_recipe_list.append(sub_rec)
        

    return jsonify({'result' : render_template('recipelist.html', recipes=passing_recipe_list)})

@app.route('/like', methods=['POST', 'GET'])
def like() :
    if current_user.is_authenticated :
        if User.query.get(current_user.get_id()).isEmailVerified == True :
            id = request.form['id'] 
            id = int(id)
            rec = Recipe.query.get(id)
            turnOtherOff = False

            if User.query.get(current_user.get_id()) in rec.users_liked :
                rec.users_liked.remove(User.query.get(current_user.get_id()))
                db.session.commit()
            elif User.query.get(current_user.get_id()) in rec.users_disliked :
                rec.users_disliked.remove(User.query.get(current_user.get_id()))
                rec.users_liked.append(User.query.get(current_user.get_id()))
                db.session.commit()
                turnOtherOff = True
            else :
                rec.users_liked.append(User.query.get(current_user.get_id()))
                db.session.commit()

            return jsonify({ 'like' : len(rec.users_liked), 'dislike' : len(rec.users_disliked), 'turnotheroff' : turnOtherOff })
        else :
            return redirect(url_for('emailverify'))
    else :
        return redirect(url_for('login'))

@app.route('/dislike', methods=['POST', 'GET'])
def dislike() :
    if current_user.is_authenticated :
        if User.query.get(current_user.get_id()).isEmailVerified == True :
            id = request.form['id']
            id = int(id)
            rec = Recipe.query.get(id)
            turnOtherOff = False

            if User.query.get(current_user.get_id()) in rec.users_disliked :
                rec.users_disliked.remove(User.query.get(current_user.get_id()))
                db.session.commit()
            elif User.query.get(current_user.get_id()) in rec.users_liked :
                rec.users_liked.remove(User.query.get(current_user.get_id()))
                rec.users_disliked.append(User.query.get(current_user.get_id()))
                db.session.commit()
                turnOtherOff = True
            else :
                rec.users_disliked.append(User.query.get(current_user.get_id()))
                db.session.commit()

            return jsonify({ 'like' : len(rec.users_liked), 'dislike' : len(rec.users_disliked), 'turnotheroff' : turnOtherOff })
        else :
            return redirect(url_for('emailverify'))
    else :
        return redirect(url_for('login'))

def findTotalLikes(user) :
    ans = 0
    for recipe in user.recipes_authored :
        ans = ans + len(recipe.users_liked)
    return ans

def save_pro_picture(form_picture) :
    ran_hex = secrets.token_hex(8)
    _, f_extension = os.path.splitext(form_picture.filename)
    picture_fn = ran_hex + f_extension
    picture_path = os.path.join(app.root_path, 'static/images/pro_pics', picture_fn)

    output_size = (165,165)
    i = Image.open(form_picture)
    new_i = i.resize(output_size)
    new_i.save(picture_path)

    return picture_fn

@app.route('/account', methods=['POST', 'GET'])
def account() :
    form = UpdateProfile()

    if current_user.is_authenticated :
        if User.query.get(current_user.get_id()).isEmailVerified == True :

            if form.validate_on_submit() :
                if form.profile_pic.data :
                    picture_file = save_pro_picture(form.profile_pic.data)
                    User.query.get(current_user.get_id()).propic = picture_file
                    db.session.commit()
                    
                    return redirect(url_for('account'))

            passing_my_recipe = []
            passing_liked_recipes = []

            my_recipes = User.query.get(current_user.get_id()).recipes_authored
            liked_recipes = User.query.get(current_user.get_id()).recipes_liked

            for recipe in my_recipes : 
                sub_rec = {}
                sub_rec['recipe'] = recipe
                if recipe in User.query.get(current_user.get_id()).recipes_liked :
                    sub_rec['liked'] = True
                else :
                    sub_rec['liked'] = False
                if recipe in User.query.get(current_user.get_id()).recipes_disliked :
                    sub_rec['disliked'] = True
                else :
                    sub_rec['disliked'] = False
                sub_rec['likes'] = len(recipe.users_liked)
                sub_rec['dislikes'] = len(recipe.users_disliked)
                passing_my_recipe.append(sub_rec)
            
            for recipe in liked_recipes : 
                if recipe.author != User.query.get(current_user.get_id()) :
                    sub_rec = {}
                    sub_rec['recipe'] = recipe
                    if recipe in User.query.get(current_user.get_id()).recipes_liked :
                        sub_rec['liked'] = True
                    else :
                        sub_rec['liked'] = False
                    if recipe in User.query.get(current_user.get_id()).recipes_disliked :
                        sub_rec['disliked'] = True
                    else :
                        sub_rec['disliked'] = False
                    sub_rec['likes'] = len(recipe.users_liked)
                    sub_rec['dislikes'] = len(recipe.users_disliked)
                    passing_liked_recipes.append(sub_rec)

            totalLikesRecieved = findTotalLikes(User.query.get(current_user.get_id()))

            return render_template('account.html', form=form, totalLikesRecieved=totalLikesRecieved, user=User.query.get(current_user.get_id()), my_recipe=passing_my_recipe, liked_recipes=passing_liked_recipes)
        else :
            return redirect(url_for('emailverify'))
    else :
        return redirect(url_for('login'))

def send_email(user) :
    token = user.get_token()
    msg = Message('Email Verification Request', sender='foodappverify@gmail.com', recipients=[user.email])
    msg.body = f"""Hi {user.username}, To verify your email address go to the following link  
{url_for('verifyEmail', token=token, _external=True)}
"""
    mail.send(msg)

@app.route('/emailverify', methods=['POST', 'GET'])
def emailverify():
    if current_user.is_authenticated :
        if User.query.get(current_user.get_id()).isEmailVerified :
            return redirect(url_for('home'))
        else :
            user = User.query.get(current_user.get_id())
            send_email(user)

            return render_template('emailverify.html')
    else :
        return redirect(url_for('login'))

@app.route('/verify/<token>', methods=['POST', 'GET'])
def verifyEmail(token) :
    user = User.verify_token(token)
    if user is None :
        return "Invalid token or token has expired"
    User.query.get(current_user.get_id()).isEmailVerified = True
    db.session.commit()
    flash('Email has verified', 'dark')
    flash('Welcome '+User.query.get(current_user.get_id()), 'success')
    return redirect(url_for('home'))

@app.route('/users/<username>')
def otherAccount(username) :
    if username == User.query.get(current_user.get_id()).username :
        return redirect(url_for('account'))
    else :
        user = User.query.filter_by(username=username).first()
        totalLikesRecieved = findTotalLikes(user)
        isFollowing = (User.query.get(current_user.get_id()) in user.followers.all())
        print(isFollowing)

        recipes = User.query.filter_by(username=username).first().recipes_authored

        passing_recipes = []

        for recipe in recipes : 
                sub_rec = {}
                sub_rec['recipe'] = recipe
                if recipe in User.query.get(current_user.get_id()).recipes_liked :
                    sub_rec['liked'] = True
                else :
                    sub_rec['liked'] = False
                if recipe in User.query.get(current_user.get_id()).recipes_disliked :
                    sub_rec['disliked'] = True
                else :
                    sub_rec['disliked'] = False
                sub_rec['likes'] = len(recipe.users_liked)
                sub_rec['dislikes'] = len(recipe.users_disliked)
                passing_recipes.append(sub_rec)

        return render_template('otheraccount.html', recipes_authored=passing_recipes, isFollowing=isFollowing, user=User.query.get(current_user.get_id()), otheruser=user, totalLikesRecieved=totalLikesRecieved)

@app.route('/follow', methods=['POST', 'GET'])
def followUser() :
    usrname = request.form['username']
    user = User.query.filter_by(username=usrname).first()
    if user == User.query.get(current_user.get_id()) :
        return "Invalid operation"
    else :
        if User.query.get(current_user.get_id()) in user.followers :
            user.followers.remove(User.query.get(current_user.get_id()))
            db.session.commit()
            return jsonify({ 'data' :  'Follow'})
        else :
            user.followers.append(User.query.get(current_user.get_id()))
            db.session.commit()
            return jsonify({ 'data' : 'Unfollow' })

def send_email_password(user) :
    token = user.get_token()
    msg = Message('Password Change Request', sender='foodappverify@gmail.com', recipients=[user.email])
    msg.body = f"""Hi {user.username}, To change the password go to the following link  
{url_for('password_change', token=token, _external=True)}
"""
    mail.send(msg)

@app.route('/emailpassword', methods=['POST', 'GET'])
def emailpassword() :
    if current_user.is_authenticated :
        return redirect(url_for('home'))
    else :
        form = EmailPassword()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user :
                send_email_password(user)
                return render_template('message.html')
            else :
                flash('No account is registered with the given email address', 'danger')
                return render_template('change_password.html', form=form)
        return render_template('change_password.html', form=form)

@app.route('/password/<token>', methods=['POST', 'GET'])
def password_change(token) :
    form = ChangePassword()
    user = User.verify_token(token)
    if user is None :
        return "Invalid token or token has expired"
    else :
        if form.validate_on_submit():
            user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            db.session.commit()
            return redirect(url_for('login'))
        return render_template('password.html', form=form)
