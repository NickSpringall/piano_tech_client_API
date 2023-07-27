from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.client import Client, clients_schema, client_schema
from models.technician import Technician
from init import db, ma, bcrypt
from decorators import check_if_technician


client_bp = Blueprint('clients', __name__, url_prefix='/clients')


@client_bp.route ('/')
def get_all_clients():
    stmt = db.select(Client).order_by(Client.name)
    clients = db.session.scalars(stmt)
    return clients_schema.dump(clients)

        
@client_bp.route ('/', methods = ['POST'])
@jwt_required()
@check_if_technician
def create_client():
    user = get_jwt_identity()

    body_data = request.get_json()
    client = Client(
        name = body_data.get('name'),
        address = body_data.get('address'),
        phone = body_data.get('phone'),
        email = body_data.get('email'),
        password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8'),
        technician_id = body_data.get('technician_id')
    )
    db.session.add(client)
    db.session.commit()

    return client_schema.dump(client), 201


    