import os.path
from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from .database import engine, Base, db_session

csrf = CSRFProtect()

NUM_COUNTRIES = 196


def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Country, UserCountry, Safety, Cost, CulturalValue, CovidRestrictions

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    csrf.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

