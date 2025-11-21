from flask import Blueprint
from app.controllers.internet_manager_controller import get_internet_customers_logic

internet_manager_bp = Blueprint("internet_manager_bp", __name__)

@internet_manager_bp.route("/api/internet-manager/customers", methods=["GET"])
def get_internet_customers():
    return get_internet_customers_logic()
