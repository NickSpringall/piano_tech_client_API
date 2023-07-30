from init import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp, And, Length, Range

class ClientInstrument(db.Model):
    __tablename__ = 'client_instruments'

    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String(50))
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

    model_id = fields.Integer(validate=And(
        Range(min=1, max=100000, error='model_id must not be less than 0 greater than 100,000')
    ))
    client_id = fields.Integer(validate=And(
        Range(min=1, max=100000, error='client_id must not be less than 0 greater than 100,000')
    ))
    finish_id = fields.Integer(validate=And(
        Range(min=1, max=100000, error='finish_id must not be less than 0 greater than 100,000')
    ))
    colour_id = fields.Integer(validate=And(
        Range(min=1, max=100000, error='colour_id must not be less than 0 greater than 100,000')
    ))

    serial_number = fields.String(validate=And(
        Length(min=3, error='serial_number must be at least 3 characters long'),
        Length(max=50, error='serial_number must not be more than 50 characters long')
    ))

    room = fields.String(required=True, validate=And(
        Length(min=3, error='room must be at least 3 characters long'),
        Length(max=50, error='room must not be more than 100 characters long'),
        Regexp('^[a-zA-Z0-9 ]+$', error='Only letters, spaces and numbers allowed')
    ))

    class Meta:
        fields = ('id', 'room', 'serial_number', 'model', 'client', 'finish', 'colour', 'model_id', 'client_id', 'colour_id', 'finish_id')

client_instrument_schema = ClientInstrumentSchema()
client_instruments_schema = ClientInstrumentSchema(many=True)


