import secrets
import os
from PIL import Image
from flask import Flask, render_template, url_for, redirect, flash, request, jsonify
from foodapp.models import User, Recipe, Ingredient
from foodapp import app, bcrypt, db
from foodapp.forms import RegistrationForm, LoginForm, AddRecipe
from foodapp.utils import searching_by_dish_name, filter, findRecipe
from flask_login import login_user, logout_user, current_user


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
        return redirect(url_for('home'))
    else :
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data) :
                login_user(user, remember=form.remember.data)
                flash('Login successful, Welcome ' + user.username +' !', 'success')
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
        recipes = Recipe.query.all()
        flash('Login successful, Welcome ' + User.query.get(current_user.get_id()).username +' !', 'success')
        return render_template('home.html', recipes=recipes)
    else :
        flash('Please login', 'info')
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
        flash('Please login', 'info')
        return render_template('add.html', form=form)
    else :
        return redirect(url_for('login'))

@app.route("/delete/<id>", methods=['GET', 'POST'])
def delete(id):
    recipe = Recipe.query.get(id)
    if recipe.author == User.query.get(current_user.get_id()) :
        db.session.delete(recipe)
        db.session.commit()
        return jsonify({ 'data' : 'none' })
    else :
        return "Unauthorized"

@app.route('/ingredientsearch', methods=['POST', 'GET'])
def ingredientsearch() :
    string = request.form['search']
    print(string)
    if len(string) > 0 :
        ans = filter(string)
    else :
        ans = []
    return jsonify({ "result" : ans })

@app.route('/dish', methods=['POST'])
def search_by_dish():
    dish = request.form['dish'] 
    print(dish)
    if len(dish) > 0 :
        ans = searching_by_dish_name(dish)
    else :
        ans = []
    return jsonify({'dish' : ans})

@app.route('/recipe', methods=['POST', 'GET'])
def recipeFiltering() :
    if current_user.is_authenticated :
        recipes = Recipe.query.all()
        return render_template('recipe.html')
    else :
        return redirect(url_for('login'))

@app.route('/filter', methods=['POST', 'GET'])
def filteredrecipe() :
    ing_list = request.form.getlist('info[]')
    recipe_list = findRecipe(ing_list)
    return jsonify({'result' : render_template('recipelist.html', recipes=recipe_list)})
