from init import db, ma 
from marshmallow import fields
from marshmallow.validate import Regexp, And, Length, Range
class Model(db.Model):
    __tablename__ = 'models'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    type_id = db.Column(db.Integer, db.ForeignKey('types.id'), nullable=False)
    make_id = db.Column(db.Integer, db.ForeignKey('makes.id'), nullable=False)
    manufacture_country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))

    type = db.relationship('Type', back_populates='models', cascade='all, delete')
    make = db.relationship('Make', back_populates='models', cascade='all, delete')
    manufacture_country = db.relationship('Country', back_populates='models', cascade='all, delete')
    client_instruments = db.relationship('ClientInstrument', back_populates='model')
   
class ModelSchema(ma.Schema):
    type = fields.Nested('TypeSchema')
    make = fields.Nested('MakeSchema')
    manufacture_country = fields.Nested('CountrySchema')

    name = fields.String(required=True, validate=And(
        Length(min=2, error='name must be at least 2 characters long'),
        Length(max=50, error='name must be no more than 50 characters long'),
        Regexp('^[a-zA-Z0-9 ]+$', error='only letters, spaces and numbers allowed')
    ))
    type_id = fields.Integer(required=True, validate=And(
        Range(min=1, max=100000, error='type_id must not be less than 0 greater than 100,000')
    ))
    make_id = fields.Integer(required=True, validate=And(
        Range(min=1, max=100000, error='type_id must not be less than 0 greater than 100,000')
    ))
    manufacture_country_id = fields.Integer(validate=And(
        Range(min=1, max=100000, error='manufacture_country_id must not be less than 0 greater than 100,000')
    ))


    class Meta:
        fields = ('id', 'name', 'type', 'make', 'manufacture_country')

model_schema = ModelSchema()
models_schema = ModelSchema(many=True)


