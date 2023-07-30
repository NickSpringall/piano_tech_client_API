from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from models.make import Make, make_schema, makes_schema
from init import db, ma, bcrypt
from decorators import check_if_technician

make_bp = Blueprint('makes', __name__, url_prefix='/makes')


@make_bp.route('/')
@jwt_required()
@check_if_technician
def get_all_makes():
    """
    returns all make instances on database. Takes no input. Only allows authenticated technician tokens.
    """
    stmt = db.select(Make)
    makes = db.session.scalars(stmt)
    return makes_schema.dump(makes), 201


@make_bp.route('/', methods = ['POST'])
@jwt_required()
@check_if_technician
def create_make():
    """
    Creates new make instance. Accepts input of name. Returns make instance on success. Only allows authenticated technician tokens. 
    """
    body_data = make_schema.load(request.get_json())
    make = Make(
        name=body_data.get('name'),
        country_id = body_data.get('country_id')
    )
    stmt = db.select(Make).filter_by(name=make.name)
    make_exists = db.session.scalar(stmt)
    if make_exists:
        return {"error": "make already registered"}, 401
    else: 
        db.session.add(make)
        db.session.commit()
        return make_schema.dump(make), 201


@make_bp.route('/<int:id>', methods = ['PUT', 'PATCH'])
@jwt_required()
@check_if_technician
def update_make(id):
    """
    Updates make data. Dynamic route takes id of make to be updated. Requires input of all entities to be updated and returns selected make instance on success. Only allows authenticated technician tokens.
    """
    body_data = make_schema.load(request.get_json(), partial=True)
    stmt = db.select(Make).filter_by(id=id)
    make = db.session.scalar(stmt)
    if make:
        make.name = body_data.get('name') or make.name
        make.country_id = body_data.get('country_id') or make.country_id
    else:
        return {'error': f'no finish found with id {id}'}, 404
    db.session.commit()
    return make_schema.dump(make), 200


@make_bp.route ('/<int:id>', methods = ['DELETE'])
@jwt_required()
@check_if_technician
def delete_make(id):
    """
    Delete one make instance. Only allows authenticated technician tokens. Dynamic route takes id of make to be deleted. Returns statement of success or failure to find make.
    """
    stmt = db.select(Make).filter_by(id=id)
    make = db.session.scalar(stmt)
    if make:
        db.session.delete(make)
        db.session.commit()
        return {'message': f'make with id {make.id} successfully deleted'}, 200
    else:
        return {'error': f'no make found with id {id}'}, 404