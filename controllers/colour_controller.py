from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from models.colour import Colour, colours_schema, colour_schema
from init import db, ma, bcrypt
from decorators import check_if_technician

colour_bp = Blueprint('colours', __name__, url_prefix='/colours')


@colour_bp.route('/')
@jwt_required()
@check_if_technician
def get_all_colours():
    """
    returns all colour instances on database. Takes no input. Only allows authenticated technician tokens.
    """
    stmt = db.select(Colour)
    colours = db.session.scalars(stmt)
    return colours_schema.dump(colours), 201


@colour_bp.route('/', methods = ['POST'])
@jwt_required()
@check_if_technician
def create_colour():
    """
    Creates new colour instance. Accepts input of colour_name. Returns colour instance on success. Only allows authenticated technician tokens. 
    """
    body_data = colour_schema.load(request.get_json())
    colour = Colour(
        colour_name=body_data.get('colour_name')
    )
    stmt = db.select(Colour).filter_by(colour_name=colour.colour_name)
    colour_exists = db.session.scalar(stmt)
    if colour_exists:
        return {"error": "colour already registered"}, 401
    else: 
        db.session.add(colour)
        db.session.commit()
        return colour_schema.dump(colour), 201


@colour_bp.route('/<int:id>', methods = ['PUT', 'PATCH'])
@jwt_required()
@check_if_technician
def update_colour(id):
    """
    Updates colour data. Dynamic route takes id of colour to be updated. Requires input of all entities to be updated and returns selected colour instance on success. Only allows authenticated technician tokens.
    """
    body_data = colour_schema.load(request.get_json(), partial=True)
    stmt = db.select(Colour).filter_by(id=id)
    colour = db.session.scalar(stmt)
    if colour:
        colour.colour_name = body_data.get('colour_name') or colour.colour_name
    else:
        return {'error': f'no colour found with id {id}'}, 404
    db.session.commit()
    return colour_schema.dump(colour), 200


@colour_bp.route ('/<int:id>', methods = ['DELETE'])
@jwt_required()
@check_if_technician
def delete_colour(id):
    """
    Delete one colour instance. Only allows authenticated technician tokens. Dynamic route takes id of colour to be deleted. Returns statement of success or failure to find colour.
    """
    stmt = db.select(Colour).filter_by(id=id)
    colour = db.session.scalar(stmt)
    if colour:
        db.session.delete(colour)
        db.session.commit()
        return {'message': f'colour with id {colour.id} successfully deleted'}, 200
    else:
        return {'error': f'no colour found with id {id}'}, 404