from init import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp, And, Length

class ClientInstrument(db.Model):
    __tablename__ = 'client_instruments'

    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String(100))
    serial_number = db.Column(db.String(50))

    model_id = db.Column(db.Integer, db.ForeignKey('models.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    finish_id = db.Column(db.Integer, db.ForeignKey('finishes.id'))
    colour_id = db.Column(db.Integer, db.ForeignKey('colours.id'))


    model = db.relationship('Model', back_populates='client_instruments')
    client = db.relationship('Client', back_populates='client_instruments')
    finish = db.relationship('Finish', back_populates='client_instruments')
    colour = db.relationship('Colour', back_populates='client_instruments')


class ClientInstrumentSchema(ma.Schema):
    model = fields.Nested('ModelSchema')
    client = fields.Nested('ClientSchema', exclude=['password', 'client_instruments'])
    finish = fields.Nested('FinishSchema')
    colour = fields.Nested('ColourSchema')

    model_id = fields.String(required=True, validate=And(
        Regexp('^[1-9]\d*$', error='only numbers can be used for model_id')
    ))
    client_id = fields.String(required=True, validate=And(
        Regexp('^[1-9]\d*$', error='only numbers can be used for model_id')
    ))
    finish_id = fields.String(validate=And(
        Regexp('^[1-9]\d*$', error='only numbers can be used for model_id')
    ))
    colour_id = fields.String(validate=And(
        Regexp('^[1-9]\d*$', error='only numbers can be used for model_id')
    ))

    serial_number = fields.String(validate=And(
        Length(min=2, error='serial_number must be at least 2 characters long'),
        Length(max=50, error='serial_number must not be more than 50 characters long')
    ))

    room = fields.String(required=True, validate=And(
        Length(min=2, error='room must be at least 2 characters long'),
        Length(max=100, error='room must not be more than 100 characters long')
    ))

    class Meta:
        fields = ('id', 'room', 'serial_number', 'model', 'client', 'finish', 'colour', 'model_id', 'client_id', 'colour_id', 'finish_id')

client_instrument_schema = ClientInstrumentSchema()
client_instruments_schema = ClientInstrumentSchema(many=True)


