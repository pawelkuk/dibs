import sys
import os

sys.path.insert(0, os.getcwd())
from pprint import pprint

pprint(sys.path)
from flask import Flask, request
from booking.domain import model
from booking.adapters import orm
from booking.service_layer import services, unit_of_work

app = Flask(__name__)
orm.start_mappers()

@app.route("/make-reservation", methods=["POST"])
def make_reservation():
    try:
        services.make_reservation(
            customer_id=request.json["customer_id"],
            screening_id=request.json["screening_id"],
            reservation_number=request.json["reservation_number"],
            seats_data=request.json["seats_data"],
            uow=unit_of_work.SqlAlchemyUnitOfWork(),
        )
    except model.SeatsCollide as e:
        return {"message": str(e)}, 400
    return "OK", 201


@app.route("/cancel-reservation", methods=["POST"])
def cancel_reservation():
    try:
        services.cancel_reservation(
            reservation_number=request.json["customer_id"],
            screening_id=request.json["screening_id"],
            uow=unit_of_work.SqlAlchemyUnitOfWork(),
        )
    except model.ReservationDoesNotExists as e:
        return {"message": str(e)}, 404

    return "OK", 204
