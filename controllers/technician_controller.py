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
# @jwt_required
# @check_if_technician
def technician_clients(id):
    stmt = db.select(Technician).filter_by(id=id)
    technician = db.session.scalar(stmt)
    if technician:
        return technician
    else:
        return
        clients = Client.query.filter_by(technician_id=id)
        return clients_schema.dump(clients)

@technician_bp.route ('/', methods = ['POST'])
@jwt_required()
@check_if_technician
def create_technician():
    body_data = request.get_json()
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
 
# @technician_bp.route ('<int:technician_id>', methods = ['PUT', 'PATCH'])
# @jwt_required
# @check_if_technician
# def update_technician_details(technician_id):
#     body_data = request.get_json()
#     stmt = db.select(Technician.filter_by(id=technician_id))
#     technician = db.session.scalar(stmt)
#     if technician:
#         if str(technician.technician_id) == get_jwt_identity():
#             return {'JWT works'} 

