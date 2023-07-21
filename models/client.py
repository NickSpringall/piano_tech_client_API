from init import db, ma
from marshmallow import fields

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100))
    phone = db.Column(db.String(30))
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String, nullable=False)

    technician = db.relationship('technicians', back_populates='clients', cascade='all, delete') 

class ClientSchema(ma.Schema):
    technician = fields.List(fields.Nested('TechnicianSchema', exclude=['password']))

    class Meta:
        fields = ('id', 'address', 'phone', 'email', 'password', 'technician')

client_schema = ClientSchema()
clients_schema = ClientSchema(many=True) 