from init import db, ma 
from marshmallow import fields

class Make(db.Model):
    __tablename__ = 'makes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))
    country = db.relationship('Country', back_populates='makes', cascade='all, delete')
    models = db.relationship('Model', back_populates='make', cascade='all, delete')


class MakeSchema(ma.Schema):
    country = fields.Nested('CountrySchema')

    class Meta:
        fields = ('id', 'name', 'country')

make_schema = MakeSchema
makes_schema = MakeSchema(many=True)