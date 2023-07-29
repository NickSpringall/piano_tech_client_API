from init import db, ma 
from marshmallow import fields

class Finish(db.Model):
    __tablename__ = 'finishes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    client_instruments = db.relationship('ClientInstrument', back_populates='finish', cascade='all, delete')

class FinishSchema(ma.Schema):
    client_instruments = fields.Nested('FinishSchema')

    class Meta:
        fields = ('id', 'name')

finish_schema = FinishSchema()
finishes_schema = FinishSchema(many = True)

