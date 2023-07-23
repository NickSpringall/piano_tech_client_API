from flask import Blueprint
from init import db
from models.technician import Technician, technician_schema, technicians_schema
from models.client import Client, clients_schema, client_schema

technician_bp = Blueprint('technicians', __name__, url_prefix='/technicians')


@technician_bp.route ('/')
def get_all_technicians():
    stmt = db.select(Technician).order_by(Technician.first_name)
    technicians = db.session.scalars(stmt)
    return technicians_schema.dump(technicians)


@technician_bp.route ('/<int:id>/clients')
def technician_clients(id):
    stmt = db.select(Technician).filter_by(id=id)
    technician = db.session.scalar(stmt)
    if technician:
        clients = Client.query.filter_by(technician_id=id)
        return clients_schema.dump(clients)
