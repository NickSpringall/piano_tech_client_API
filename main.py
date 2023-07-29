from flask import Flask
import os
from init import db, ma, bcrypt, jwt
from flask_sqlalchemy import SQLAlchemy
from marshmallow.exceptions import ValidationError
from controllers.cli_controller import db_commands
from controllers.client_controller import client_bp
from controllers.technician_controller import technician_bp
from controllers.auth_controllers.tech_auth_controller import auth_technician_bp
from controllers.auth_controllers.client_auth_controller import client_auth_bp
from controllers.client_instrument_controller import client_instrument_bp
from controllers.colour_controller import colour_bp
from controllers.country_controller import country_bp
from controllers.finish_controller import finish_bp
from controllers.make_controller import make_bp
from controllers.type_controller import type_bp
from controllers.model_controller import model_bp

from sqlalchemy.exc import IntegrityError, DataError
from psycopg2 import errorcodes

def create_app():
    app = Flask (__name__)

    app.config.from_object("config.app_config")
    app.config["JWT_SECRET_KEY"]=os.environ.get("JWT_SECRET_KEY")

    @app.errorhandler(IntegrityError)
    def validation_error(err):
        if err.orig.pgcode == errorcodes.FOREIGN_KEY_VIOLATION:
            return {'error': f'{err.orig.diag.constraint_name} was not found, please enter a valid id'}
        elif err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {'error': f'{err.orig.diag.column_name} field cannot be empty'}
        
    @app.errorhandler(DataError)
    def data_error(err):
        if err.orig.pgcode == errorcodes.STRING_DATA_RIGHT_TRUNCATION:
            return{'error':  err.orig.args}
        else:
            return{'error': 'something went wrong'}

    @app.errorhandler(ValueError)
    def value_error(err):
        return {'error': str(err)}

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
    app.register_blueprint(country_bp)
    app.register_blueprint(finish_bp)
    app.register_blueprint(make_bp)
    app.register_blueprint(type_bp)
    app.register_blueprint(model_bp)


    return app
    