from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from models.client import Client, client_schema, clients_schema_no_pw, client_schema_no_pw
from init import db, ma, bcrypt
from decorators import check_if_technician, check_if_technician_or_logged_in_client
from .client_instrument_controller import client_instrument_bp


client_bp = Blueprint('clients', __name__, url_prefix='/clients')

@client_bp.route ('/')
@jwt_required()
@check_if_technician
def get_all_clients():
    """
    returns a list of all clients' data on the database, takes no input. Only allows authenticated technician tokens.
    """
    stmt = db.select(Client).order_by(Client.name)
    clients = db.session.scalars(stmt)
    return clients_schema_no_pw.dump(clients), 200


@client_bp.route ('<int:id>')
@jwt_required()
@check_if_technician_or_logged_in_client
def get_single_client(id):
    """
    returns all data for a single client, dynamic route takes the id of the client to be returned. Authenticated technicians can view any client. Authenticated clients can only view their own data
    """
    stmt = db.select(Client).filter_by(id=id)
    client = db.session.scalar(stmt)
    if client:
        return client_schema_no_pw.dump(client), 200
    else:
        return {'error': 'no client found, please check you have the correct client id'}, 404


@client_bp.route ('/<int:id>', methods = ['PUT', 'PATCH'])
@jwt_required()
@check_if_technician
def update_client_details(id):
    """
    updates an existing clients' details.  Only allows authenticated technician tokens. Expects input from client of all client fields to be updated and checks them against the schema constraints. On successful registration returns updated and unchanged client data without password.
    """
    body_data = client_schema.load(request.get_json(), partial=True)
    stmt = db.select(Client).filter_by(id=id)
    client = db.session.scalar(stmt)
    if client:
        client.name = body_data.get('name') or client.name
        client.address = body_data.get('address') or client.address
        client.phone = body_data.get('phone') or client.phone
        client.email = body_data.get('email') or client.email
        client.technician_id = body_data.get('technician_id') or client.technician_id
        try:
            client.password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8')
        except: ValueError
    else:
        return {'error': f'no client found with id {id}'}, 404
    
    db.session.commit()
    return client_schema_no_pw.dump(client), 200
    


@client_bp.route ('/<int:id>', methods = ['DELETE'])
@jwt_required()
@check_if_technician
def delete_client(id):
    """
    delete one client's data. Only allows authenticated technician tokens. Dynamic route takes id of client to be deleted. returns statement of success or failure to find client
    """
    stmt = db.select(Client).filter_by(id=id)
    client = db.session.scalar(stmt)
    if client:
        db.session.delete(client)
        db.session.commit()
        return {'message': f'client {client.name} successfully deleted'}, 200
    else:
        return {'error': f'no client found with id {id}'}, 404