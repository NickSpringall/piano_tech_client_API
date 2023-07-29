from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from models.model import Model, model_schema, models_schema
from init import db, ma, bcrypt
from decorators import check_if_technician

model_bp = Blueprint('models', __name__, url_prefix='/models')

@model_bp.route('/')
@jwt_required()
@check_if_technician
def get_all_models():
    stmt = db.select(Model)
    models = db.session.scalars(stmt)
    return models_schema.dump(models), 201

@model_bp.route('/<int:id>')
@jwt_required()
@check_if_technician
def get_models_for_make(id):
    stmt = db.select(Model).filter_by(make_id=id)
    models = db.session.scalars(stmt)
    return models_schema.dump(models)
    

@model_bp.route('/', methods = ['POST'])
@jwt_required()
@check_if_technician
def create_model():
    body_data = model_schema.load(request.get_json())
    model = Model(
        name=body_data.get('name'),
        type_id=body_data.get('type_id'),
        make_id=body_data.get('make_id'),
        manufacturer_country_id=body_data.get('manufacture_country_id')
    )
    stmt = db.select(Model).filter_by(name=model.name)
    model_exists = db.session.scalar(stmt)
    if model_exists:
        return {"error": "model already registered"}, 401
    else: 
        db.session.add(model)
        db.session.commit()

        return model_schema.dump(model), 201


@model_bp.route('/<int:id>', methods = ['PUT', 'PATCH'])
@jwt_required()
@check_if_technician
def update_model(id):
    body_data = model_schema.load(request.get_json(), partial=True)
    stmt = db.select(Model).filter_by(id=id)
    model = db.session.scalar(stmt)
    if model:
        model.name = body_data.get('name') or model.name
        model.type_id = body_data.get('type_id') or model.type_id
        model.make_id = body_data.get('make_id') or model.make_id
        model.manufacturer_country_id = body_data.get('manufacturer_country_id') or model.manufacturer_country_id
    else:
        return {'error': f'no model found with id {id}'}, 404
    
    db.session.commit()
    return model_schema.dump(model)

@model_bp.route ('/<int:id>', methods = ['DELETE'])
@jwt_required()
@check_if_technician
def delete_model(id):
    stmt = db.select(Model).filter_by(id=id)
    model = db.session.scalar(stmt)
    if model:
        db.session.delete(model)
        db.session.commit()
        return {'message': f'model with id {model.id} successfully deleted'}, 200
    else:
        return {'error': f'no model found with id {id}'}, 404