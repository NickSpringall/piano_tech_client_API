from init import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp, And, Length, Range


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
    technician = fields.Nested('TechnicianSchema', exclude=['password', 'clients', 'id'])
    client_instruments = fields.List(fields.Nested('ClientInstrumentSchema', exclude=['client']))

    technician_id = fields.Integer(validate=And(
        Range(min=1, max=100000, error='technician_id must not be less than 0 greater than 100,000')
    ))

    email = fields.String(required=True, validate=And(
        Length(min=2, error='name must be at least 2 characters long'),
        Length(max=100, error='email must be no more than 100 characters long')
    ))

    class Meta:
        fields = ('id', 'name', 'address', 'phone', 'email', 'technician', 'client_instruments', 'password', 'technician_id')

client_schema_no_pw = ClientSchema(exclude=['password'])
clients_schema_no_pw = ClientSchema(many=True, exclude=['password']) 

client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)
