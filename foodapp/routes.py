from flask import Flask, render_template, url_for, redirect, flash
from foodapp import app, bcrypt, db
from foodapp.forms import RegistrationForm, LoginForm
from foodapp.models import User

@app.route("/", methods=['GET', 'POST'])
def reg():
    form=RegistrationForm()
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
    return render_template('home.html');
    

