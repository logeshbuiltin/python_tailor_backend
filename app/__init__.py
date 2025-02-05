from flask import Flask
from app.extensions import db, jwt
from app.routes import register_routes
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()  # Load environment variables
    app = Flask(__name__)

    # Configure the app
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Register routes
    register_routes(app)

    return app
