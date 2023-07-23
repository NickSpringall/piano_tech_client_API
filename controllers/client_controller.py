from flask import Blueprint, request
from init import db, bcrypt
from models.client import Client, clients_schema, client_schema
from models.technician import Technician

client_bp = Blueprint('clients', __name__, url_prefix='/clients')


@client_bp.route ('/')
def get_all_clients():
    stmt = db.select(Client).order_by(Client.name)
    clients = db.session.scalars(stmt)
    return clients_schema.dump(clients)

@client_bp.route ('/', methods = ['POST'])
def create_client():
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