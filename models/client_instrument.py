from init import db, ma
from marshmallow import fields

class ClientInstrument(db.Model):
    __tablename__ = 'client_instruments'

    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String(100))

    model_id = db.Column(db.Integer, db.ForeignKey('models.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
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

    class Meta:
        fields = ('id', 'room', 'model', 'client', 'finish', 'colour')

client_instrument_schema = ClientInstrumentSchema()
client_instruments_schema = ClientInstrumentSchema(many=True)


