from init import db, ma 
from marshmallow import fields

class Model(db.Model):
    __tablename__ = 'models'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    type_id = db.Column(db.Integer, db.ForeignKey('types.id'))
    make_id = db.Column(db.Integer, db.ForeignKey('makes.id'))
    manufacture_country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))

    type = db.relationship('Type', back_populates='models', cascade='all, delete')
    make = db.relationship('Make', back_populates='models', cascade='all, delete')
    manufacture_country = db.relationship('Country', back_populates='models', cascade='all, delete')
   
class ModelSchema(ma.Schema):
    type = fields.Nested('TypeSchema')
    make = fields.Nested('MakeSchema')
    manufacture_country = fields.Nested('CountrySchema')

    class Meta:
        fields = ('id', 'name', 'type', 'make', 'manufacture_country')

model_schema = ModelSchema()
models_schema = ModelSchema(many=True)


