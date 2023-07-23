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


    model = db.relationship('models', back_populates='client_instruments')
    client = db.relationship('clients', back_populates='client_instruments')
    finish = db.relationship('finishes', back_populates='client_instruments')
    colour = db.relationship('colours', back_populates='client_instruments')


class ClientInstrumentSchema(ma.Schema):
    pass



