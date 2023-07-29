from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from models.type import Type, type_schema, types_schema
from init import db, ma, bcrypt
from decorators import check_if_technician

type_bp = Blueprint('types', __name__, url_prefix='/types')


@type_bp.route('/')
@jwt_required()
@check_if_technician
def get_all_types():
    stmt = db.select(Type)
    types = db.session.scalars(stmt)
    return types_schema.dump(types), 201


@type_bp.route('/', methods = ['POST'])
@jwt_required()
@check_if_technician
def create_type():
    body_data = type_schema.load(request.get_json())
    finish = Type(
        name=body_data.get('name')
    )
    stmt = db.select(Type).filter_by(name=type.name)
    type_exists = db.session.scalar(stmt)
    if type_exists:
        return {"error": "type already registered"}, 401
    else: 
        db.session.add(type)
        db.session.commit()

        return type_schema.dump(finish), 201


@type_bp.route('/<int:id>', methods = ['PUT', 'PATCH'])
@jwt_required()
@check_if_technician
def update_type(id):
    body_data = type_schema.load(request.get_json(), partial=True)
    stmt = db.select(Type).filter_by(id=id)
    type = db.session.scalar(stmt)
    if type:
        type.name = body_data.get('name') or type.name
    else:
        return {'error': f'no type found with id {id}'}, 404
    
    db.session.commit()
    return type_schema.dump(type), 200


@type_bp.route ('/<int:id>', methods = ['DELETE'])
@jwt_required()
@check_if_technician
def delete_type(id):
    stmt = db.select(Type).filter_by(id=id)
    type = db.session.scalar(stmt)
    if type:
        db.session.delete(type)
        db.session.commit()
        return {'message': f'type with id {type.id} successfully deleted'}, 200
    else:
        return {'error': f'no type found with id {id}'}, 404