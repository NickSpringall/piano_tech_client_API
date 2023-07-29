from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from models.finish import Finish, finish_schema, finishes_schema
from init import db, ma, bcrypt
from decorators import check_if_technician

finish_bp = Blueprint('finishes', __name__, url_prefix='/finishes')


@finish_bp.route('/')
@jwt_required()
@check_if_technician
def get_all_finishes():
    stmt = db.select(Finish)
    finishes = db.session.scalars(stmt)
    return finishes_schema.dump(finishes), 201


@finish_bp.route('/', methods = ['POST'])
@jwt_required()
@check_if_technician
def create_finish():
    body_data = finish_schema.load(request.get_json())
    finish = Finish(
        name=body_data.get('name')
    )
    stmt = db.select(Finish).filter_by(name=finish.name)
    finish_exists = db.session.scalar(stmt)
    if finish_exists:
        return {"error": "finish already registered"}, 401
    else: 
        db.session.add(finish)
        db.session.commit()
        return finish_schema.dump(finish), 201


@finish_bp.route('/<int:id>', methods = ['PUT', 'PATCH'])
@jwt_required()
@check_if_technician
def update_finish(id):
    body_data = finish_schema.load(request.get_json(), partial=True)
    stmt = db.select(Finish).filter_by(id=id)
    finish = db.session.scalar(stmt)
    if finish:
        finish.name = body_data.get('name') or finish.name
    else:
        return {'error': f'no finish found with id {id}'}, 404
    db.session.commit()
    return finish_schema.dump(finish), 200


@finish_bp.route ('/<int:id>', methods = ['DELETE'])
@jwt_required()
@check_if_technician
def delete_finish(id):
    stmt = db.select(Finish).filter_by(id=id)
    finish = db.session.scalar(stmt)
    if finish:
        db.session.delete(finish)
        db.session.commit()
        return {'message': f'finish with id {finish.id} successfully deleted'}, 200
    else:
        return {'error': f'no finish found with id {id}'}, 404