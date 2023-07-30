from init import db, ma 
from marshmallow import fields
from marshmallow.validate import Regexp, And, Length

class Finish(db.Model):
    __tablename__ = 'finishes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    client_instruments = db.relationship('ClientInstrument', back_populates='finish', cascade='all, delete')

class FinishSchema(ma.Schema):
    client_instruments = fields.Nested('FinishSchema')

    name = fields.String(required=True, validate=And(
        Length(min=2, error='name must be at least 2 characters long'),
        Length(max=100, error='name must be no more than 100 characters long'),
        Regexp('^[a-zA-Z0-9 ]+$', error='only letters, spaces and numbers allowed')
    ))

    class Meta:
        fields = ('id', 'name')

finish_schema = FinishSchema()
finishes_schema = FinishSchema(many = True)

