from flask import Blueprint
from init import db
from models.client import Client, clients_schema, client_schema
from models.technician import Technician

client_bp = Blueprint('clients', __name__, url_prefix='/clients')


@client_bp.route ('/')
def get_all_clients():
    stmt = db.select(Client).order_by(Client.name)
    clients = db.session.scalars(stmt)
    return clients_schema.dump(clients)