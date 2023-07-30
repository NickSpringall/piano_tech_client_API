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
        Length(min=2, error='first_name must be at least 2 characters long'),
        Length(max=100, error='first_name must be no more than 100 characters long'),
        Regexp('^[a-zA-Z0-9 ]+$', error='only letters, spaces and numbers allowed')
    ))
    last_name = fields.String(required=True, validate=And(
        Length(min=2, error='last_name must be at least 2 characters long'),
        Length(max=100, error='last_name must be no more than 100 characters long'),
        Regexp('^[a-zA-Z0-9 ]+$', error='only letters, spaces and numbers allowed')
    ))
    address = fields.String(validate=And(
        Length(min=10, error='address must be at least 10 characters long'),
        Length(max=100, error='address must be no mare than 100 characters long')
    ))
    phone = fields.String(validate=And(
        Length(min=2, error='phone must be at least 2 characters long'),
        Length(max=30, error='phone must be no more than 30 characters long')
    ))
    email = fields.String(required=True, validate=And(
        Length(min=2, error='email must be at least 2 characters long'),
        Length(max=100, error='email must be no more than 100 characters long')
    ))


    class Meta:
        fields = ('id', 'first_name', 'last_name', 'address', 'phone', 'email', 'password', 'clients')
    
technician_schema_no_pw = TechnicianSchema(exclude=['password'])
technicians_schema_no_pw = TechnicianSchema(many=True, exclude=['password'])

technician_schema = TechnicianSchema()
technicians_schema = TechnicianSchema(many=True)
