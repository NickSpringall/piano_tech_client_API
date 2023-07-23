from init import db, ma 
from marshmallow import fields

class Country(db.Model):
    __tablename__ = 'countries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    makes = db.relationship('Make', back_populates='country', cascade='all, delete')
    models = db.relationship('Model', back_populates='manufacture_country', cascade='all, delete')

class CountrySchema(ma.Schema):
    makes = fields.List(fields.Nested('MakesSchema'))

    class Meta():
        fields = ('id', 'name')

country_schema = CountrySchema
countries_schema = CountrySchema(many=True)

