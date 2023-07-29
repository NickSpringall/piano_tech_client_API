from flask import Blueprint, request
from init import db, bcrypt
from models.technician import Technician, technician_schema, technicians_schema
from models.client import Client, clients_schema, client_schema
from decorators import check_if_technician
from flask_jwt_extended import jwt_required, get_jwt_identity

technician_bp = Blueprint('technicians', __name__, url_prefix='/technicians')


@technician_bp.route ('/')
@jwt_required()
@check_if_technician
def get_all_technicians():
    stmt = db.select(Technician).order_by(Technician.first_name)
    technicians = db.session.scalars(stmt)
    return technicians_schema.dump(technicians)


@technician_bp.route ('/<int:id>/clients')
@jwt_required()
@check_if_technician
def technician_clients(id):
    stmt = db.select(Technician).filter_by(id=id)
    technician = db.session.scalar(stmt)
    if technician:
        clients = Client.query.filter_by(technician_id=id)
        return clients_schema.dump(clients)
    else:
        return {"error": f"technician with id {id} does not exist"}, 404


@technician_bp.route ('/', methods = ['POST'])
@jwt_required()
@check_if_technician
def create_technician():
    body_data = technician_schema.load(request.get_json())
    technician = Technician(
        first_name=body_data.get('first_name'),
        last_name=body_data.get('last_name'),
        address=body_data.get('address'),
        phone=body_data.get('phone'),
        email=body_data.get('email'),
        password=bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8')
    )
    stmt = db.select(Technician). filter_by(email=technician.email)
    tech_exists = db.session.scalar(stmt)
    if tech_exists:
        return {"error": "email already in use"}, 401     
    else:   
        db.session.add(technician)
        db.session.commit()

        return technician_schema.dump(technician), 201
 

@technician_bp.route ('<int:id>', methods = ['PUT', 'PATCH'])
@jwt_required()
@check_if_technician
def update_technician_details(id):
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
        return technician_schema.dump(technician)
    else:
        return {'error': f'no technician found with id {id}'}, 404
    
    
@technician_bp.route ('<int:id>', methods = ['DELETE'])
@jwt_required()
@check_if_technician
def delete_technician(id):
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