from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
import json


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = json.loads(request.data) 
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                login_user(user, remember=True)
                #Redirect to admin portal
                return jsonify({"message":"Successfully logged in"}), 200
            else:
                return jsonify({"message":"incorrect password, please try again"}), 401
        else:
            return jsonify({"message":"User does not exist"}), 404
    # Redirect to home
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    # Redirect to home
    return jsonify({"message":"Successfully logged out"}), 200
