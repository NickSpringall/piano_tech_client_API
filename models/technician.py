from init import db, ma
from marshmallow import fields

class Technician(db.Model):
    __tablename__ = "technicians"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    address = db.Column(db.String(100))
    phone = db.Column(db.String(30))
    email = db.Column(db.String(100))
    password = db.Column(db.String, nullable=False)

class TechnicianSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'address', 'phone', 'email', 'password')
    
technician_schema = TechnicianSchema()
technicians_schema = TechnicianSchema(many=True)