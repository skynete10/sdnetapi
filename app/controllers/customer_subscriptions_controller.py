# app/controllers/customer_subscriptions_controller.py

from decimal import Decimal

from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError

from app.connections import get_db
from app.models.customers_model import Customer,CustomerSubscription
from app.models.services_model import Service


def save_customer_subscription_logic(data: dict):
    """
    Create or update a customer subscription.

    Expected payload:
    {
        "id": optional, for edit
        "customer_username": str,
        "service_code": str,
        "price": str | number   # <-- matches frontend
    }
    """
    required = ["customer_username", "service_code", "amount"]
    missing = [f for f in required if not str(data.get(f, "")).strip()]

    if missing:
        return jsonify({
            "error": "Validation failed",
            "missing_fields": missing
        }), 400

    customer_username = str(data.get("customer_username", "")).strip()
    service_code = str(data.get("service_code", "")).strip()

    # validate price (stored in DB as 'amount')
    try:
        amount = Decimal(str(data.get("amount", "0")).strip())
    except Exception:
        return jsonify({"error": "amount must be numeric"}), 400

    if amount < 0:
        return jsonify({"error": "amount cannot be negative"}), 400

    db = get_db()
    s = db.get_session()

    try:
        sub_id = data.get("id")

        if sub_id:
            # UPDATE
            subscription = (
                s.query(CustomerSubscription)
                .filter_by(id=sub_id)
                .first()
            )
            if not subscription:
                return jsonify({"error": "Subscription not found"}), 404
        else:
            # CREATE
            subscription = CustomerSubscription(
                customer_username=customer_username,
                service_code=service_code,
                amount=amount,   # DB column is 'amount'
            )
            s.add(subscription)

        # common fields
        subscription.customer_username = customer_username
        subscription.service_code = service_code
        subscription.amount = amount

        s.commit()

        return jsonify({
            "status": "success",
            "id": subscription.id
        }), (201 if not sub_id else 200)

    except SQLAlchemyError as e:
        s.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        s.close()


def get_customer_subscriptions_logic():
    """
    Returns subscriptions with customer + service info:
    [
      {
        "id": ...,
        "customer_username": "...",
        "customer_fullname": "...",
        "service_code": "...",
        "service_name": "...",
        "price": float
      },
      ...
    ]
    """
    db = get_db()
    s = db.get_session()

    try:
        rows = (
            s.query(
                CustomerSubscription.id,
                Customer.username.label("customer_username"),
                Customer.fullname.label("customer_fullname"),
                Service.service_code,
                Service.service_name,
                CustomerSubscription.amount,
            )
            .join(
                Customer,
                Customer.username == CustomerSubscription.customer_username,
            )
            .join(
                Service,
                Service.service_code == CustomerSubscription.service_code,
            )
            .order_by(Customer.fullname, Service.service_name)
            .all()
        )

        result = [
            {
                "id": r.id,
                "customer_username": r.customer_username,
                "customer_fullname": r.customer_fullname or "",
                "service_code": r.service_code,
                "service_name": r.service_name or "",
                # send 'price' to match frontend interface
                "price": float(r.amount) if r.amount is not None else 0.0,
            }
            for r in rows
        ]

        return jsonify(result), 200

    finally:
        s.close()
