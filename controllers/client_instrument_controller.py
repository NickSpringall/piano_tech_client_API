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
    stmt = db.select(ClientInstrument).order_by(ClientInstrument.client_id)
    instruments = db.session.scalars(stmt)
    return client_instruments_schema.dump(instruments)


@client_instrument_bp.route ('/<int:id>')
@jwt_required()
@check_if_technician_or_logged_in_client
def get_single_client_instruments(id):
    stmt = db.select(ClientInstrument).filter_by(client_id=id)
    instruments = db.session.scalars(stmt)
    return client_instruments_schema.dump(instruments)

@client_instrument_bp.route ('/<int:id>', methods = ['DELETE'])
@jwt_required()
@check_if_technician
def delete_client_instrument(id):
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
    body_data = client_instrument_schema.load(request.get_json())
    instrument = ClientInstrument(
        room = body_data.get('room'),
        model_id = body_data.get('model_id'),
        client_id = body_data.get('client_id'),
        finish_id = body_data.get('finish_id'),
        colour_id = body_data.get('colour_id')
        )
    db.session.add(instrument)
    db.session.commit()
    return client_instrument_schema.dump(instrument), 201
    

@client_instrument_bp.route ('/<int:id>', methods = ['PUT', 'PATCH'])
@jwt_required()
@check_if_technician
def update_client_instrument(id):
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
    return client_instrument_schema.dump(instrument)
   