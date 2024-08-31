from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required

from .. import app, db
from ..forms import LoginForm, RegistrationForm, EditProfileForm
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

@app.route('/profile/edit', methods = ['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        user: User = User.query.filter_by(id = current_user.get_id()).first()
        new_username = form.username.data or user.name
        password, confirm_pwd = form.password.data, form.confirm_password.data

        if password and confirm_pwd:
            new_password = sha256_crypt.hash(form.new_password.data)
            user.passwd = new_password
        user.name = new_username
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('auth/edit_profile.html', form = form)