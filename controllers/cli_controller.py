from flask import Blueprint
from init import db, bcrypt
from models.technician import Technician
from models.client import Client
from models.country import Country
from models.make import Make
from models.type import Type
from models.model import Model
from models.colour import Colour
from models.client_instrument import ClientInstrument
from models.finish import Finish


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

    colours = [
        Colour(
        colour_name = 'Black'
        ),
        Colour(
        colour_name = 'Walnut'
        ),
        Colour(
        colour_name = 'Mahogany'
        ),
        Colour(
        colour_name = 'White'
        )
    ]
    db.session.add_all(colours)

    models = [
        Model(
        name = 'C1',
        type = types[1],
        make = makes[0],
        manufacture_country = countries[0]
        ),
        Model(
        name = 'U3',
        type = types[0],
        make = makes[0],
        manufacture_country = countries[0]
        ),
        Model(
        name = 'U1J',
        type = types[0],
        make = makes[0],
        manufacture_country = countries[3]
        ),
        Model(
        name = 'M',
        type = types[1],
        make = makes[1],
        manufacture_country = countries[4]
        )
    ]
    db.session.add_all(models)

    finishes = [
        Finish(
        name = 'gloss polyester'
        ),
        Finish(
        name = 'matte lacquer'
        ),
        Finish(
        name = 'french polish'
        ),
        Finish(
        name = 'hand rubbed polyester'
        )
    ]
    db.session.add_all(finishes)

    client_instruments = [
        ClientInstrument(
        room = 'music room',
        serial_number = '6,238,223',
        model = models[2],
        client = clients[0],
        finish = finishes[1],
        colour = colours[0]
        ),
        ClientInstrument(
        room = 'music room',
        serial_number = 'K843223B',
        model = models[2],
        client = clients[0],
        finish = finishes[0],
        colour = colours[0]
        ),
        ClientInstrument(
        room = 'teaching studio 1',
        serial_number = 'LU229933',
        model = models[2],
        client = clients[0],
        finish = finishes[1],
        colour = colours[3]
        ),
        ClientInstrument(
        room = 'drama room',
        serial_number = '203944',
        model = models[0],
        client = clients[1],
        finish = finishes[3],
        colour = colours[0]
        ),
        ClientInstrument(
        room = 'theatre',
        serial_number = '33222ML2',
        model = models[3],
        client = clients[1],
        finish = finishes[1],
        colour = colours[1]
        )
    ]
    db.session.add_all(client_instruments)

    db.session.commit()

    print('Tables Seeded')