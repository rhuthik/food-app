from flask import Flask, render_template, url_for, redirect, flash, request, jsonify
from foodapp import app, bcrypt, db
from foodapp.forms import RegistrationForm, LoginForm, AddRecipe
from foodapp.models import User, Recipe, Ingredient

def filter(string) :
    shortList = []
    counter = 0
    for i in Ingredient.query.all() :
        if string.capitalize() in (i.name).capitalize() :
            counter += 1
            shortList.append(i.name)
        if counter == 10 :
            break
    return shortList

@app.route("/", methods=['GET', 'POST'])
def reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hash_pwd)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route("/home", methods=['GET', 'POST'])
def home():
    recipes = Recipe.query.all()
    return render_template('home.html', recipes=recipes);

@app.route("/add", methods=['GET', 'POST'])
def add():
    form = AddRecipe()
    theCheckList = []
    if request.method == 'POST':
        theCheckList = request.form.getlist('ingredient')
    if form.validate_on_submit():
        recipe = Recipe(name=form.recipe_name.data, procedure=form.procedure.data)
        db.session.add(recipe)
        db.session.commit()
        
        for i in theCheckList:
            ing = Ingredient.query.get(i)
            recipe.ingredients.append(ing)
            db.session.commit()

        return redirect(url_for('home'))

    return render_template('add.html', form=form)

@app.route("/delete/<id>", methods=['GET', 'POST'])
def delete(id):
    recipe = Recipe.query.get(id)
    db.session.delete(recipe)
    db.session.commit()

    return redirect(url_for('home'))

@app.route('/process', methods=['POST', 'GET'])
def process() :
    string = request.form['search']
    print(string)
    if len(string) > 0 :
        ans = filter(string)
    else :
        ans = []
    return jsonify({ "result" : ans })

@app.route("/upvote/<id>", methods=['GET', 'POST'])
def upvote_incr(id):
    recipe = Recipe.query.get(id)
    recipe.upvotes = recipe.upvotes + 1
    db.session.commit()

    return redirect(url_for('home'))

@app.route("/downvote/<id>", methods=['GET', 'POST'])
def downvote_incr(id):
    recipe = Recipe.query.get(id)
    recipe.downvotes = recipe.downvotes + 1
    db.session.commit()
    
    return redirect(url_for('home'))
