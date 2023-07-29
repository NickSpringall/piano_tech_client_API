from flask import Blueprint, request
from init import db, bcrypt
from models.technician import Technician, technician_schema_no_pw,technician_schema
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta
from decorators import check_if_technician

auth_technician_bp = Blueprint('auth_technician', __name__, url_prefix='/auth_tech')


@auth_technician_bp.route ('/', methods = ['POST'])
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
        return technician_schema_no_pw.dump(technician), 201
    

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
            return {'error': 'Incorrect password'}, 401
    else: 
        return {'error': 'No user with this email'}, 401

