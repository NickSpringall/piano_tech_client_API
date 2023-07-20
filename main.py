from flask import Flask
import os
from init import db, ma, bcrypt, jwt
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask (__name__)

    app.config.from_object("config.app_config")
    app.config["JWT_SECRET_KEY"]=os.environ.get("JWT_SECRET_KEY")

    @app.route('/')
    def hello_world():
        return 'Hello, World!'
    
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    return app
    