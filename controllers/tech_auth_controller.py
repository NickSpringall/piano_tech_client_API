from flask import Blueprint, request
from init import db, bcrypt
from models.technician import Technician, technician_schema, technicians_schema
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from datetime import timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/auth_tech')

@auth_bp.route('/register', methods=['POST'])
def auth_login():
    body_data = request.get_json()
    
    technician = Technician()
    technician.first_name = body_data.get('first_name')
    technician.last_name = body_data.get('last_name')
    technician.address = body_data.get('address')
    technician.phone = body_data.get('phone')
    technician.email = body_data.get('email')
    if body_data.get('password'):
       technician.password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8')
    
    db.session.add(technician)
    db.session.commit()

    return technician_schema.dump(technician), 201

@auth_bp.route('/login', methods=['POST'])
def auth_tech_login():
    body_data = request.get_json()

    stmt = db.select(Technician).filter_by(email=body_data.get('email'))
    technician = db.session.scalar(stmt)
    if technician:
        if bcrypt.check_password_hash(technician.password, body_data.get('password')):
            token = create_access_token(identity=('technician' + str(technician.id)), expires_delta=timedelta(days=1))
            return {'email': technician.email, 'token': token}
        else: 
            return {'error': 'Incorrect password'}
    else: 
        return {'error': 'No user with this email'}

