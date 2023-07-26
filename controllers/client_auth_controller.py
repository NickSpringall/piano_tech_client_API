from flask import Blueprint, request
from init import db, bcrypt
from models.technician import Technician, technician_schema, technicians_schema
from models.client import Client, client_schema, clients_schema
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from datetime import timedelta

client_auth_bp = Blueprint('auth', __name__, url_prefix='/auth_client')

@client_auth_bp('/login', methods=['POST'])
def auth_client_login():
    body_data = request.get_json()

    stmt = db.select(Client).filter_by(email=body_data.get('email'))
    client = db.session.scalar(stmt)
    if client:
        if bcrypt.check_password_hash(client.password, body_data.get('password')):
            token = create_access_token(identity=('client' + str(client.id)), exipres_delta=timedelta(days=1))
            return {'email': client.email, 'token': token}
        else:
            return {'error': 'Incorrect password'}
    else:
        return {'error': 'no user with this email'}

