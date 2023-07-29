from init import db, ma 
from marshmallow import fields
from marshmallow.validate import Regexp, And, Length

class Type(db.Model):
    __tablename__ = 'types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    models = db.relationship('Model', back_populates='type', cascade='all, delete')

class TypeSchema(ma.Schema):
    models = fields.List(fields.Nested('ModelsSchema'))

    name = fields.String(required=True, validate=And(
        Length(min=2, error='Title must be at least 2 characters long'),
        Regexp('^[a-zA-Z0-9 ]+$', error='only letters, spaces and numbers allowed')
    ))

    class Meta():
        fields = ('id', 'name')

type_schema = TypeSchema
types_schema = TypeSchema(many=True)