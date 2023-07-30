from init import db, ma 
from marshmallow import fields
from marshmallow.validate import Regexp, And, Length, Range

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
        Length(min=2, error='name must be at least 2 characters long'),
        Length(max=50, error='name must be no more than 50 characters long'),
        Regexp('^[a-zA-Z0-9 ]+$', error='only letters, spaces and numbers allowed')
    ))
    country_id = fields.Integer(validate=And(
        Range(min=1, max=100000, error='technician_id must not be less than 0 greater than 100,000')
    ))

    class Meta:
        fields = ('id', 'name', 'country')

make_schema = MakeSchema
makes_schema = MakeSchema(many=True)