from init import db, ma
from marshmallow import fields

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
   

class ClientSchema(ma.Schema):
    technician = fields.Nested('TechnicianSchema', exclude=['password'])

    class Meta:
        fields = ('id', 'address', 'phone', 'email', 'technician', 'password')

client_schema = ClientSchema(exclude=['password'])
clients_schema = ClientSchema(many=True, exclude=['password']) 