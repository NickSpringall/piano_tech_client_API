from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from models.colour import Colour, colours_schema, colour_schema
from init import db, ma, bcrypt
from decorators import check_if_technician, check_if_technician_or_logged_in_client

colour_bp = Blueprint('colours', __name__, url_prefix='/colours')

@colour_bp.route('/')
@jwt_required()
@check_if_technician
def get_all_colours():
    stmt = db.select(Colour)
    colours = db.session.scalars(stmt)
    return colours_schema.dump(colours), 201

@colour_bp.route('/', methods = ['POST'])
@jwt_required()
@check_if_technician
def create_colour():
    body_data = request.get_json()
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
    body_data = request.get_json()
    colour = Colour