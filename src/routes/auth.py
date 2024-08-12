from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_user, logout_user

from .. import app, db
from ..forms import LoginForm, RegistrationForm
from ..models import User

from passlib.hash import sha256_crypt

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name = form.username.data).first()
        if user and sha256_crypt.verify(form.password.data, user.passwd):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
    return render_template('auth/login.html', form = form)

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Adding the user to the database
        hashed_password = sha256_crypt.hash(form.password.data)
        user = User(
            name = form.username.data,
            passwd = hashed_password
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('auth/signup.html', form = form)

@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('home'))