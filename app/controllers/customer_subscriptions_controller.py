# app/controllers/customer_subscriptions_controller.py

from decimal import Decimal

from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError

from app.connections import get_db
from app.models.customers_model import Customer,CustomerSubscription
from app.models.services_model import Service
from datetime import datetime, date


def save_customer_subscription_logic(data: dict):
    required = ["customer_username", "service_code", "amount"]
    missing = [f for f in required if not str(data.get(f, "")).strip()]
    if missing:
        return jsonify({"error": "Validation failed", "missing_fields": missing}), 400

    customer_username = str(data.get("customer_username", "")).strip()
    service_code = str(data.get("service_code", "")).strip()

    try:
        amount = Decimal(str(data.get("amount", "0")).strip())
    except Exception:
        return jsonify({"error": "amount must be numeric"}), 400

    if amount < 0:
        return jsonify({"error": "amount cannot be negative"}), 400

    billing_date_raw = str(data.get("billing_date", "")).strip()
    billing_date_value = None
    if billing_date_raw:
        try:
            billing_date_value = datetime.strptime(billing_date_raw, "%Y-%m-%d").date()
        except Exception:
            return jsonify({"error": "billing_date must be in YYYY-MM-DD format"}), 400

    manager_empcode_raw = data.get("manager_empcode")
    manager_empcode_value = str(manager_empcode_raw).strip() if manager_empcode_raw else None

    # ======================================================
    #  SIMPLE LOGIC:
    #  if "stopped" → 0
    #  else → 1
    # ======================================================
    raw_status = data.get("subscription_status", data.get("status", None))

    if raw_status is None:
        subscription_status_value = 1  # default active
    else:
        raw = str(raw_status).strip().lower()
        subscription_status_value = 0 if raw == "stopped" else 1
    # ======================================================

    db = get_db()
    s = db.get_session()

    try:
        sub_id = data.get("id")

        if sub_id:
            subscription = s.query(CustomerSubscription).filter_by(id=sub_id).first()
            if not subscription:
                return jsonify({"error": "Subscription not found"}), 404

            exists_for_customer = (
                s.query(CustomerSubscription)
                .filter(
                    CustomerSubscription.customer_username == customer_username,
                    CustomerSubscription.id != sub_id
                )
                .first()
            )
            if exists_for_customer:
                return jsonify({"error": "This client already has a subscription."}), 409

        else:
            exists_for_customer = (
                s.query(CustomerSubscription)
                .filter_by(customer_username=customer_username)
                .first()
            )
            if exists_for_customer:
                return jsonify({"error": "This client already has a subscription."}), 409

            subscription = CustomerSubscription(
                customer_username=customer_username,
                service_code=service_code,
                amount=amount,
                billing_date=billing_date_value,
                subscription_status=subscription_status_value,
            )
            s.add(subscription)

        subscription.customer_username = customer_username
        subscription.service_code = service_code
        subscription.amount = amount

        if billing_date_raw:
            subscription.billing_date = billing_date_value

        subscription.emp_manager = manager_empcode_value
        subscription.subscription_status = subscription_status_value

        s.commit()

        return jsonify({"status": "success", "id": subscription.id}), (
            201 if not sub_id else 200
        )

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
                CustomerSubscription.emp_manager,
                CustomerSubscription.subscription_status,
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
                "emp_manager": r.emp_manager or "",
                "subscription_status": r.subscription_status or "",
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

def delete_subscription_logic(sub_id: int):
    """
    Delete a customer subscription by ID.
    """

    db = get_db()
    s = db.get_session()

    try:
        sub = s.query(CustomerSubscription).filter_by(id=sub_id).first()

        if not sub:
            return jsonify({"error": "Subscription not found"}), 404

        s.delete(sub)
        s.commit()

        return jsonify({"success": True, "deleted_id": sub_id}), 200

    except SQLAlchemyError as e:
        s.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        s.close()
