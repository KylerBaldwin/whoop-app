from os import path, getenv
from datetime import timedelta

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager

from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
    # Ensure session cookies persist and are secure
    app.config['SESSION_COOKIE_SECURE'] = True  # Requires HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True  # Protect against XSS
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Allows OAuth redirect flow
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)  # Short TTL
    db.init_app(app)
    CORS(app, supports_credentials=True)

    from .routes import routes
    from .auth import auth

    app.register_blueprint(routes, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, WhoopAuth
    
    with app.app_context():
        db.drop_all()
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
