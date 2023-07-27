from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from models.client import Client, clients_schema, client_schema
from init import db, ma, bcrypt
from decorators import check_if_technician, check_if_technician_or_logged_in_client


client_bp = Blueprint('clients', __name__, url_prefix='/clients')


@client_bp.route ('/')
@jwt_required()
@check_if_technician
def get_all_clients():
    stmt = db.select(Client).order_by(Client.name)
    clients = db.session.scalars(stmt)
    return clients_schema.dump(clients)


@client_bp.route ('/<int:id>')
@jwt_required()
@check_if_technician_or_logged_in_client
def get_single_client(id):
    stmt = db.select(Client).filter_by(id=id)
    client = db.session.scalar(stmt)
    return client_schema.dump(client)

        
@client_bp.route ('/', methods = ['POST'])
@jwt_required()
@check_if_technician
def create_client():
    body_data = request.get_json()
    client = Client(
        name = body_data.get('name'),
        address = body_data.get('address'),
        phone = body_data.get('phone'),
        email = body_data.get('email'),
        technician_id = body_data.get('technician_id'),
        password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8')    
    )
    db.session.add(client)
    db.session.commit()

    return client_schema.dump(client), 201


@client_bp.route ('/<int:id>', methods = ['PUT', 'PATCH'])
@jwt_required()
@check_if_technician
def update_client_details(id):
    body_data = request.get_json()
    stmt = db.select(Client).filter_by(id=id)
    client = db.session.scalar(stmt)
    if client:
        client.name = body_data('name') or client.name
        client.address = body_data('address') or client.address
        client.phone = body_data('phone') or client.phone
        client.email = body_data('email') or client.email
        client.technician = body_data('technician') or client.technician
        try:
            client.password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8')
        except: ValueError
    else:
        return {'error': f'no client found with id {id}'}, 404


@client_bp.route ('/<int:id>', methods = ['DELETE'])
@jwt_required()
@check_if_technician
def delete_client(id):
    stmt = db.select(Client).filter_by(id=id)
    client = db.session.scalar(stmt)
    if client:
        db.session.delete(client)
        db.session.commit()
        return {'message': f'client {client.name} successfully deleted'}, 200
    else:
        return {'error': f'no client found with id {id}'}, 404