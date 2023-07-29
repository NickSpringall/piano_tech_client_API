from flask import Blueprint, request
from init import db, bcrypt
from models.technician import Technician
from flask_jwt_extended import create_access_token
from datetime import timedelta

auth_technician_bp = Blueprint('auth_technician', __name__, url_prefix='/auth_tech')


@auth_technician_bp.route('/login', methods=['POST'])
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

