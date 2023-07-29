from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from models.country import Country, countries_schema, country_schema
from init import db, ma, bcrypt
from decorators import check_if_technician

country_bp = Blueprint('countries', __name__, url_prefix='/countries')

@country_bp.route('/')
@jwt_required()
@check_if_technician
def get_all_countries():
    stmt = db.select(Country)
    countries = db.session.scalars(stmt)
    return countries_schema.dump(countries), 201

@country_bp.route('/', methods = ['POST'])
@jwt_required()
@check_if_technician
def create_country():
    body_data = request.get_json()
    country = Country(
        name=body_data.get('name')
    )
    stmt = db.select(Country).filter_by(name=country.name)
    country_exists = db.session.scalar(stmt)
    if country_exists:
        return {"error": "country already registered"}, 401
    else: 
        db.session.add(country)
        db.session.commit()

        return country_schema.dump(country), 201

@country_bp.route('/<int:id>', methods = ['PUT', 'PATCH'])
@jwt_required()
@check_if_technician
def update_country(id):
    body_data = request.get_json()
    stmt = db.select(Country).filter_by(id=id)
    country = db.session.scalar(stmt)
    if country:
        country.name = body_data.get('name') or country.name
    else:
        return {'error': f'no country found with id {id}'}, 404
    
    db.session.commit()
    return country_schema.dump(country)


@country_bp.route ('/<int:id>', methods = ['DELETE'])
@jwt_required()
@check_if_technician
def delete_country(id):
    stmt = db.select(Country).filter_by(id=id)
    country = db.session.scalar(stmt)
    if country:
        db.session.delete(country)
        db.session.commit()
        return {'message': f'country with id {country.id} successfully deleted'}, 200
    else:
        return {'error': f'no country found with id {id}'}, 404