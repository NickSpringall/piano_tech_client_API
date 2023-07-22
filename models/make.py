from init import db, ma 

class Make(db.Model):
    __tablename__ = 'makes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))
    country = db.relationship('Country', back_populates='makes', cascade='all, delete')

