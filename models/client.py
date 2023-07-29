from init import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp, And, Length


class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(100))
    phone = db.Column(db.String(30))
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String, nullable=False)

    technician_id = db.Column(db.Integer, db.ForeignKey('technicians.id'))

    technician = db.relationship('Technician', back_populates='clients', cascade='all, delete') 
    client_instruments = db.relationship('ClientInstrument', back_populates='client', cascade='all, delete')
   

class ClientSchema(ma.Schema):
    technician = fields.Nested('TechnicianSchema', exclude=['password', 'clients'])
    client_instruments = fields.List(fields.Nested('ClientInstrumentSchema', exclude=['client']))

    technician_id = fields.String(validate=And(
        Regexp('^[1-9]\d*$', error='only numbers can be used for technician_id')
    ))

    email = fields.String(required=True, validate=And(
        Length(min=2, error='name must be at least 2 characters long'),
        Regexp('^[a-zA-Z0-9 ]+$', error='only letters, spaces and numbers allowed')
    ))
    
    class Meta:
        fields = ('id', 'name', 'address', 'phone', 'email', 'technician', 'client_instruments', 'password', 'technician_id')

client_schema = ClientSchema(exclude=['password'])
clients_schema = ClientSchema(many=True, exclude=['password']) 