from flask import Blueprint, request
from init import db, bcrypt
from models.technician import Technician, technician_schema, technicians_schema
from models.client import Client, clients_schema, client_schema

technician_bp = Blueprint('technicians', __name__, url_prefix='/technicians')

@technician_bp.route ('/')
def get_all_technicians():
    stmt = db.select(Technician).order_by(Technician.first_name)
    technicians = db.session.scalars(stmt)
    return technicians_schema.dump(technicians)


@technician_bp.route ('/', methods = ['POST'])
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
 

@technician_bp.route ('/<int:id>/clients')
def technician_clients(id):
    stmt = db.select(Technician).filter_by(id=id)
    technician = db.session.scalar(stmt)
    if technician:
        clients = Client.query.filter_by(technician_id=id)
        return clients_schema.dump(clients)