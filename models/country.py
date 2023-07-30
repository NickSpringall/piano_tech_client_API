from init import db, ma 
from marshmallow import fields
from marshmallow.validate import Regexp, And, Length

class Country(db.Model):
    __tablename__ = 'countries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    makes = db.relationship('Make', back_populates='country', cascade='all, delete')
    models = db.relationship('Model', back_populates='manufacture_country', cascade='all, delete')

class CountrySchema(ma.Schema):
    makes = fields.List(fields.Nested('MakesSchema'))

    name = fields.String(required=True, validate=And(
        Length(min=3, error='Title must be at least 3 characters long'),
        Regexp('^[a-zA-Z0-9 ]+$', error='only letters, spaces and numbers allowed')
    ))

    class Meta():
        fields = ('id', 'name')

country_schema = CountrySchema
countries_schema = CountrySchema(many=True)

