# app/routes/customers_routes.py
from flask import Blueprint
from app.controllers import customers_controller

customers_bp = Blueprint("customers_bp", __name__)

@customers_bp.route("/api/customers", methods=["GET"])
def get_customers_route():
    return customers_controller.get_customers()


@customers_bp.route("/api/customers/import-excel", methods=["POST"])
def import_customers_excel_route():
    return customers_controller.import_customers_excel()


@customers_bp.route("/api/customers/savecustomer", methods=["POST"])
def save_customer_route():
    return customers_controller.save_customer()


@customers_bp.route("/api/customers/count", methods=["GET"])
def customers_count_route():
    return customers_controller.customers_count()
