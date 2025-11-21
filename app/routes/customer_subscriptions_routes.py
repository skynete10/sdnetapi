# app/routes/customer_subscriptions_routes.py

from flask import Blueprint, request, jsonify

from app.controllers.customer_subscriptions_controller import (
    save_customer_subscription_logic,
    get_customer_subscriptions_logic,
)

customer_subscriptions_bp = Blueprint("customer_subscriptions_bp", __name__)


@customer_subscriptions_bp.post("/api/customer-subscriptions/savesubscription")
def save_customer_subscription_route():
    data = request.get_json() or {}
    return save_customer_subscription_logic(data)


@customer_subscriptions_bp.get("/api/customer-subscriptions")
def get_customer_subscriptions_route():
    return get_customer_subscriptions_logic()
