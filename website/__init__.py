import os.path
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from .database import engine, Base, db_session

csrf = CSRFProtect()
mail = Mail()

env = os.getenv('ENVIRONMENT')

NUM_COUNTRIES = 196


def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

    mail.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Country, UserCountry, Safety, Cost, CulturalValue, CovidRestrictions

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    csrf.init_app(app)

    # So that every new request will clean up the session, avoiding rollback errors
    # It also avoids sessions overlapping and causing errors
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

