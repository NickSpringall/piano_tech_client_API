from flask import Blueprint
from init import db, bcrypt
from models.technician import Technician
from models.client import Client
from models.country import Country
from models.make import Make
from models.type import Type
from models.model import Model


db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print("Tables Created")

@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print('Tables Dropped')

@db_commands.cli.command('seed')
def seed_db():
    technicians = [
        Technician(
            first_name='James',
            last_name='Smith',
            address= '5 smith st, smithville',
            phone= '0483 293 399',
            email='james_smith@email.com',
            password=bcrypt.generate_password_hash('jamessmith').decode('utf-8')
        ),
        Technician(
            first_name='Sally',
            last_name='Ford',
            address='20 street st, streetville',
            phone= '0495 438 393',
            email='sally@email.com',
            password=bcrypt.generate_password_hash('sallyford').decode('utf-8')
        )
    ]

    db.session.add_all(technicians)
    
    clients = [
        Client(
            name='Toorak College',
            address='6 Toorak rd, Toorak',
            phone='03 9374 3733',
            email='info@toorakcollege.com',
            password=bcrypt.generate_password_hash('toorak').decode('utf-8'),
            technician=technicians[0]
        ),
        Client(
        name='Elsternwick State School',
        address='4390 St Kilda rd, Elsternwick',
        phone='03 9283 3933',
        email='info@ess.gov.edu.au',
        password=bcrypt.generate_password_hash('ess').decode('utf-8'),
        technician=technicians[0]
        )
    ]

    db.session.add_all(clients)

    countries = [
        Country(
        name = 'Japan'
        ),
        Country(
        name = 'China'
        ),
        Country(
        name = 'USA'
        ),
        Country(
        name = 'Indonesia'
        ),
        Country(
        name = 'Germany'
        )
    ]

    db.session.add_all(countries)

    makes = [
        Make(
        name = 'Yamaha',
        country = countries[0]
        ),
        Make(
        name = 'Steinway',
        country = countries[4]
        )
    ]

    db.session.add_all(makes)

    types = [
        Type(
        name = 'upright'   
        ),
        Type(
        name = 'grand'
        )
    ]
    db.session.add_all(types)

    db.session.commit()

    print('Tables Seeded')