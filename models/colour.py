from init import db, ma 
from marshmallow import fields
from marshmallow.validate import Regexp, And, Length

class Colour(db.Model):
    __tablename__ = 'colours'

    id = db.Column(db.Integer, primary_key=True)
    colour_name = db.Column(db.String(50))

    client_instruments = db.relationship('ClientInstrument', back_populates='colour', cascade='all, delete')

class ColourSchema(ma.Schema):
    colour_name = fields.String(required=True, validate=And(
        Length(min=2, error='colour_name must be at least 2 characters long'),
        Length(max=50, error='colour_name must be no more than 100 characters long'),
        Regexp('^[a-zA-Z0-9 ]+$', error='only letters, spaces and numbers allowed')
    ))

    class Meta:
        fields = ('id', 'colour_name')

colour_schema = ColourSchema()
colours_schema = ColourSchema(many=True)