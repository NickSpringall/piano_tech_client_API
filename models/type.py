from init import db, ma 
from marshmallow import fields

class Type(db.Model):
    __tablename__ = 'types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    models = db.relationship('Model', back_populates='type', cascade='all, delete')

class TypeSchema(ma.Schema):
    models = fields.List(fields.Nested('ModelsSchema'))

    class Meta():
        fields = ('id', 'name')

type_schema = TypeSchema
types_schema = TypeSchema(many=True)