# app/routes/services_routes.py

from flask import Blueprint, request, jsonify
from app.controllers.services_controller import (
  save_service_logic,
  get_services_logic,
  get_next_service_code_logic,
)

services_bp = Blueprint("services_bp", __name__)


@services_bp.post("/api/services/saveservice")
def save_service_route():
    data = request.get_json() or {}
    return save_service_logic(data)


@services_bp.get("/api/services")
def get_services_route():
    return get_services_logic()


@services_bp.get("/api/services/maxcode")
def get_services_maxcode_route():
    return get_next_service_code_logic()
