from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models.parent import Parent
from .models.child import Child
from .models.transaction import Transaction
from .models.goal import Goal
from .models.chore import Chore
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        user = Parent.query.filter_by(name=name).first()
        if user:
            if decryptData(user.password) == password:
                flash('Logged in successfully!'+ str(user.getChildren()), category='success')
                login_user(user, remember=True)

                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            user = Child.query.filter_by(name=name).first()
            if user:
                if decryptData(user.password) == password:
                    flash('Logged in successfully!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Incorrect password, try again.', category='error')
            else:
                flash('Name does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/create-child', methods=['GET', 'POST'])
def create_child():
    if request.method == 'POST':
        name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        dob = request.form.get('date')
        balance = request.form.get('balance')
        print(name, password1, password2, dob, balance)

        child_user = Child.query.filter_by(name=name).first()
        user = Parent.query.filter_by(name=name).first()
        if user is not None and child_user is not None:
             flash('Please enter a different name. An account with this name already exists. You can enter a username or add your last name.', category='error')           
        if len(name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 3:
            flash('Password must be at least 3 characters.', category='error')
        else:
            new_user = Child(name=name, password=encryptData(password1), dob=dob, balance=balance)
            db.session.add(new_user)
            current_user.addChild(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("create_child.html", user=current_user)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        child_user = Child.query.filter_by(name=name).first()
        user = Parent.query.filter_by(name=name).first()
        if user is not None or child_user is not None:
             flash('Please enter a different name. An account with this name already exists. You can enter a username or add your last name.', category='error')           
        elif len(name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 3:
            flash('Password must be at least 3 characters.', category='error')
        else:
            new_user = Parent(name=name, password=encryptData(password1))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


def encryptData(data):
    encrypted = "";

    for x in data:
        a = ord(x);
        a = a + 41;
        encrypted = encrypted + chr(a);
    
    return encrypted;

def decryptData(data):
    decrypted = "";

    for x in data:
        a = ord(x);
        a = a - 41;
        decrypted = decrypted + chr(a);
    
    return decrypted;