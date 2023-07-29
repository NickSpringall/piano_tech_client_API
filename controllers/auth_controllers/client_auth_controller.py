from flask import Blueprint, request
from init import db, bcrypt
from models.client import Client, client_schema_no_pw, client_schema
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta
from decorators import check_if_technician

client_auth_bp = Blueprint('auth_client', __name__, url_prefix='/auth_client')
 

@client_auth_bp.route ('/', methods = ['POST'])
@jwt_required()
@check_if_technician
def create_client():
    body_data = client_schema.load(request.get_json())
    client = Client(
        name = body_data.get('name'),
        address = body_data.get('address'),
        phone = body_data.get('phone'),
        email = body_data.get('email'),
        technician_id = body_data.get('technician_id'),
        password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8')    
    )
    stmt = db.select(Client).filter_by(email=client.email)
    client_exists = db.session.scalar(stmt)
    if client_exists:
        return {"error": "client already registered"}, 405
    else:
        db.session.add(client)
        db.session.commit()
        return client_schema_no_pw.dump(client), 201


@client_auth_bp.route('/login', methods=['POST'])
def auth_client_login():
    body_data = request.get_json()

    stmt = db.select(Client).filter_by(email=body_data.get('email'))
    client = db.session.scalar(stmt)
    if client:
        if bcrypt.check_password_hash(client.password, body_data.get('password')):
            token = create_access_token(identity=('client' + str(client.id)), expires_delta=timedelta(days=1))
            return {'email': client.email, 'token': token}
        else:
            return {'error': 'Incorrect password'}, 401
    else:
        return {'error': 'no user with this email'}, 401

