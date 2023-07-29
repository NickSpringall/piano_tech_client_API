from init import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp, And, Length

class Technician(db.Model):
    __tablename__ = "technicians"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100))
    phone = db.Column(db.String(30))
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String, nullable=False)

    clients = db.relationship('Client', back_populates='technician', cascade='all, delete')


class TechnicianSchema(ma.Schema):
    clients = fields.List(fields.Nested('ClientSchema', exclude=['password', 'technician']))

    first_name = fields.String(required=True, validate=And(
        Length(min=2, error='name must be at least 2 characters long'),
        Regexp('^[a-zA-Z0-9 ]+$', error='only letters, spaces and numbers allowed')
    ))
    last_name = fields.String(required=True, validate=And(
        Length(min=2, error='name must be at least 2 characters long'),
        Regexp('^[a-zA-Z0-9 ]+$', error='only letters, spaces and numbers allowed')
    ))
    address = fields.String(validate=And(
        Length(min=2, error='name must be at least 2 characters long'),
    ))
    phone = fields.String(validate=And(
        Length(min=2, error='name must be at least 2 characters long'),
    ))
    email = fields.String(required=True, validate=And(
        Length(min=2, error='name must be at least 2 characters long'),
    ))


    class Meta:
        fields = ('id', 'first_name', 'last_name', 'address', 'phone', 'email', 'password', 'clients')
    
technician_schema_no_pw = TechnicianSchema(exclude=['password'])
technicians_schema_no_pw = TechnicianSchema(many=True, exclude=['password'])

technician_schema = TechnicianSchema()
technicians_schema = TechnicianSchema(many=True)
