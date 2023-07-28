from flask import Flask
import os
from init import db, ma, bcrypt, jwt
from flask_sqlalchemy import SQLAlchemy
from controllers.cli_controller import db_commands
from controllers.client_controller import client_bp
from controllers.technician_controller import technician_bp
from controllers.auth_controllers.tech_auth_controller import auth_technician_bp
from controllers.auth_controllers.client_auth_controller import client_auth_bp
from controllers.client_instrument_controller import client_instrument_bp
from controllers.colour_controller import colour_bp

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

    app.register_blueprint(db_commands)
    app.register_blueprint(client_bp)
    app.register_blueprint(technician_bp)
    app.register_blueprint(auth_technician_bp)
    app.register_blueprint(client_auth_bp)
    app.register_blueprint(client_instrument_bp)
    app.register_blueprint(colour_bp)

    return app
    