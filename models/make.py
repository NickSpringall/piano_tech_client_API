from init import db, ma 
from marshmallow import fields
from marshmallow.validate import Regexp, And, Length

class Make(db.Model):
    __tablename__ = 'makes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))
    country = db.relationship('Country', back_populates='makes', cascade='all, delete')
    models = db.relationship('Model', back_populates='make', cascade='all, delete')

    

class MakeSchema(ma.Schema):
    country = fields.Nested('CountrySchema')

    name = fields.String(required=True, validate=And(
        Length(min=2, error='Title must be at least 2 characters long'),
        Regexp('^[a-zA-Z0-9 ]+$', error='only letters, spaces and numbers allowed')
    ))
    country_id = fields.String(validate=And(
        Regexp('^[1-9]\d*$', error='only numbers can be used for country_id')
    ))

    class Meta:
        fields = ('id', 'name', 'country')

make_schema = MakeSchema
makes_schema = MakeSchema(many=True)