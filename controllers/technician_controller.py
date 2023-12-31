from flask import Blueprint, request
from init import db, bcrypt
from models.technician import Technician, technician_schema, technicians_schema, technician_schema_no_pw, technicians_schema_no_pw
from models.client import Client, clients_schema, client_schema, clients_schema_no_pw
from decorators import check_if_technician
from flask_jwt_extended import jwt_required, get_jwt_identity

technician_bp = Blueprint('technicians', __name__, url_prefix='/technicians')


@technician_bp.route ('/')
@jwt_required()
@check_if_technician
def get_all_technicians():
    """
    returns all technician instances on database. Takes no input. Only allows authenticated technician tokens.
    """
    stmt = db.select(Technician).order_by(Technician.first_name)
    technicians = db.session.scalars(stmt)
    return technicians_schema_no_pw.dump(technicians), 200

@technician_bp.route ('/<int:id>')
@jwt_required()
@check_if_technician
def get_single_technician(id):
    """
    Returns a single technician instance. Dynamic route accepts id of technician to be returned. Only allows authenticated technician tokens.
    """
    stmt = db.select(Technician).filter_by(id=id)
    technician = db.session.scalar(stmt)
    if technician:
        return technician_schema.dump(technician), 200
    else:
        return {'error': 'no client found, please check you have the correct client id'}, 404


@technician_bp.route ('/<int:id>/clients')
@jwt_required()
@check_if_technician
def technician_clients(id):
    """
    Returns all clients for a given technician instance. Dynamic route accepts id of technician who's client instances will be returned. Only allows authenticated technician tokens.
    """
    stmt = db.select(Technician).filter_by(id=id)
    technician = db.session.scalar(stmt)
    if technician:
        clients = technician.clients
        if clients:
            client_list = Client.query.filter_by(technician_id=id)
            return clients_schema_no_pw.dump(client_list)
        else:
            return {'message': f'technician with id {id} does not have any clients'}, 200
    else:
        return {"error": f"technician with id {id} does not exist"}, 404


@technician_bp.route ('<int:id>', methods = ['PUT', 'PATCH'])
@jwt_required()
@check_if_technician
def update_technician_details(id):
    """
    Updates one technician instance data. Dynamic route takes id of technician instance to be updated. Requires input of all entities to be updated and returns selected technician instance on success. Only allows authenticated technician tokens.
    """
    body_data = technician_schema.load(request.get_json(), partial=True)
    stmt = db.select(Technician).filter_by(id=id)
    technician = db.session.scalar(stmt)
    if technician:
        if ("technician" + str(technician.id)) != get_jwt_identity():
            return {'error': 'Technicians can only edit their own information'}, 403
        technician.first_name = body_data.get('first_name') or technician.first_name
        technician.last_name = body_data.get('last_name') or technician.last_name
        technician.address = body_data.get('address') or technician.address
        technician.phone = body_data.get('phone') or technician.phone
        technician.email = body_data.get ('email') or technician.email
        try:
            technician.password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8')
        except: ValueError
        db.session.commit()
        return technician_schema_no_pw.dump(technician), 200
    else:
        return {'error': f'no technician found with id {id}'}, 404
    

@technician_bp.route ('<int:id>', methods = ['DELETE'])
@jwt_required()
@check_if_technician
def delete_technician(id):
    """
    Delete one technician instance. Only allows authenticated technician tokens. Dynamic route takes id of technician to be deleted. Returns statement of success or failure to find technician.
    """
    stmt = db.select(Technician).filter_by(id=id)
    technician = db.session.scalar(stmt)
    if technician:
        if ("technician" + str(technician.id)) != get_jwt_identity():
            return {'error': 'Technicians can only delete their own information'}, 403
        else:
            db.session.delete(technician)
            db.session.commit()
            return {'message': f'technician {technician.first_name} {technician.last_name} successfully deleted'}, 200
    else:
        return {'error': f'no technician found with id {id}'}, 404