from flask import Flask
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from controllers.Users import users_routes
from flask_login import LoginManager
from connectors.mysql_connectors import engine
from models.Users import User
import os

load_dotenv()
app=Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.register_blueprint(users_routes)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    return session.query(User).get(int(user_id))