from init import db, ma 
from marshmallow import fields

class Colour(db.Model):
    __tablename__ = 'colours'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    client_instruments = db.relationship('ClientInstrument', back_populates='colour', cascade='all, delete')

class ColourSchema(ma.Schema):
    client_instruments = fields.Nested('ClientInstrumentSchema')

    class Meta:
        fields = ('id', 'name', 'client_instruments')

colour_schema = ColourSchema()
colours_schema = ColourSchema(many=True)