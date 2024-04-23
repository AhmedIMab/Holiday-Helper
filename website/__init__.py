import os.path
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_login import LoginManager
from os import path


DB_NAME = "database.db"

engine = create_engine(f'sqlite:///website/{DB_NAME}')
# This is the base db session
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'XXX'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Country, UserCountry, Safety, Cost, CulturalValue, CovidRestrictions

    create_database()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database():
    if not os.path.exists(os.path.join(os.getcwd(), 'website', DB_NAME)):
        print("\nHERE, NO DATABASE DETECTED SO CREATING ONE! \n")
        Base.metadata.create_all(bind=engine)
        print("Database Created")
