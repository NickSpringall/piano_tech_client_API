from init import db, ma 

class Country(db.Model):
    __tablename__ = 'countries'

    id = db.Column(db.Integer, Primary_Key=True)
    name = db.Column(db.String(50))

class CountrySchema(ma.Schema):
    class Meta():
        fields = ('id', 'name')

country_schema = CountrySchema
countries_schema = CountrySchema(many=True)