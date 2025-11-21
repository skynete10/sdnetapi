# app/controllers/customer_subscriptions_controller.py

from decimal import Decimal

from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError

from app.connections import get_db
from app.models.customers_model import Customer,CustomerSubscription
from app.models.services_model import Service
from datetime import datetime, date


def save_customer_subscription_logic(data: dict):
    """
    Create or update a customer subscription.

    Expected payload:
    {
        "id": optional, for edit
        "customer_username": str,
        "service_code": str,
        "amount": str | number,
        "billing_date": optional str in "YYYY-MM-DD"
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

    # validate amount (stored in DB as 'amount')
    try:
        amount = Decimal(str(data.get("amount", "0")).strip())
    except Exception:
        return jsonify({"error": "amount must be numeric"}), 400

    if amount < 0:
        return jsonify({"error": "amount cannot be negative"}), 400

    # validate/parse billing_date (optional) - expects full date now
    billing_date_raw = str(data.get("billing_date", "")).strip()
    billing_date_value = None

    if billing_date_raw:
        try:
            # frontend sends "YYYY-MM-DD"
            dt = datetime.strptime(billing_date_raw, "%Y-%m-%d")
            billing_date_value = dt.date()
        except Exception:
            return jsonify({"error": "billing_date must be in YYYY-MM-DD format"}), 400

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
                amount=amount,
                billing_date=billing_date_value  # set if provided
            )
            s.add(subscription)

        # common fields (always update these)
        subscription.customer_username = customer_username
        subscription.service_code = service_code
        subscription.amount = amount

        # only overwrite billing_date if client sent it
        if billing_date_raw:
            subscription.billing_date = billing_date_value

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
                CustomerSubscription.amount.label("amount"),
                CustomerSubscription.billing_date.label("billing_date"),
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
                "amount": float(r.amount) if r.amount is not None else 0.0,
                "billing_date": (
                    r.billing_date.strftime("%Y-%m-%d")
                    if r.billing_date is not None
                    else None
                ),
                # optional if you still want it:
                # "price": float(r.amount) if r.amount is not None else 0.0,
            }
            for r in rows
        ]

        return jsonify(result), 200

    finally:
        s.close()
