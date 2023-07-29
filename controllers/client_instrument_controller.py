from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from models.client import Client, clients_schema, client_schema
from models.client_instrument import ClientInstrument, client_instrument_schema, client_instruments_schema
from init import db, ma, bcrypt
from decorators import check_if_technician, check_if_technician_or_logged_in_client


client_instrument_bp = Blueprint('client_instruments', __name__, url_prefix='/client_instruments')


@client_instrument_bp.route ('/')
@jwt_required()
@check_if_technician
def get_all_instruments():
    """
    returns a list of all client_instrument data on the database, takes no input. Only allows authenticated technician tokens
    """     
    stmt = db.select(ClientInstrument).order_by(ClientInstrument.client_id)
    instruments = db.session.scalars(stmt)
    return client_instruments_schema.dump(instruments), 200


@client_instrument_bp.route ('/<int:id>')
@jwt_required()
@check_if_technician_or_logged_in_client
def get_single_clients_instruments(id):
    """
    returns all data for a single client_instrument, dynamic route takes the id of the client_instrument to be returned. Only allows authenticated technician tokens.
    """
    stmt = db.select(Client).filter_by(id=id)
    client = db.session.scalar(stmt)
    if client:
        stmt = db.select(ClientInstrument).filter_by(client_id=id)
        instruments = db.session.scalars(stmt)
        return client_instruments_schema.dump(instruments), 200
    else:
        return {'error': 'no client found, please check you have the correct client id'}, 404



@client_instrument_bp.route ('/<int:id>', methods = ['DELETE'])
@jwt_required()
@check_if_technician
def delete_client_instrument(id):
    """
    Delete one client_instrument data. Only allows authenticated technician tokens. Dynamic route takes id of client_instrumet to be deleted. Returns statement of success or failure to find client_instrument.
    """
    stmt = db.select(ClientInstrument).filter_by(id=id)
    instrument = db.session.scalar(stmt)
    if instrument:
        db.session.delete(instrument)
        db.session.commit()
        return {'message': f'instrument with id {instrument.id} successfully deleted'}, 200
    else:
        return {'error': f'no instrument found with id {id}'}, 404


@client_instrument_bp.route ('/', methods = ['POST'])
@jwt_required()
@check_if_technician
def create_client_instrument():
    """
    Create client_instrument instance and saves to client_instrument database. Requires input of all non-nullable client_instrument entities and returns inputted data on success. Only allows authenticated technician tokens.
    """
    body_data = client_instrument_schema.load(request.get_json())
    instrument = ClientInstrument(
        room = body_data.get('room'),
        model_id = body_data.get('model_id'),
        client_id = body_data.get('client_id'),
        finish_id = body_data.get('finish_id'),
        colour_id = body_data.get('colour_id'),
        serial_number = body_data.get('serial_number')
        )
    stmt = db.select(ClientInstrument).filter_by(serial_number=instrument.serial_number)
    instrument_exists = db.session.scalar(stmt)
    if instrument_exists:
        return {'error': f'instrument with serial number {instrument.serial_number} already on system'}, 405
    else:
        db.session.add(instrument)
        db.session.commit()
        return client_instrument_schema.dump(instrument), 201
    

@client_instrument_bp.route ('/<int:id>', methods = ['PUT', 'PATCH'])
@jwt_required()
@check_if_technician
def update_client_instrument(id):
    """
    Updates client_instrument data. Dynamic route takes id of client_instrument to be updated. Requires input of all entities to be updated and returns selected client_instrument instence on success. Only allows authenticated technician tokens.
    """
    body_data = client_instrument_schema.load(request.get_json(), partial=True)
    stmt = db.select(ClientInstrument).filter_by(id=id)
    instrument = db.session.scalar(stmt)
    if instrument:
        instrument.room = body_data.get('room') or instrument.room
        instrument.model_id = body_data.get('model_id') or instrument.model_id
        instrument.client_id = body_data.get('client_id') or instrument.client_id
        instrument.finish_id = body_data.get('finish_id') or instrument.finish_id
        instrument.colour_id = body_data.get('colour_id') or instrument.colour_id
        db.session.commit()
        return client_instrument_schema.dump(instrument), 200
    else:
        return {'error': f'no instrument found with id {id}'}, 404
   