# app/controllers/services_controller.py

from flask import jsonify
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from decimal import Decimal

from app.connections import get_db
from app.models.services_model import Service


def get_next_service_code(session) -> str:
    """
    Returns the next service_code as a zero-padded string.

    Assumes service_code is numeric or numeric string (e.g., '0001', '0010').
    If there is no existing row, returns '0001'.
    """
    max_code = session.query(func.max(Service.service_code)).scalar()

    if not max_code:
        return "0001"

    try:
        length = len(max_code)
        num = int(max_code)
        next_num = num + 1
        return str(next_num).zfill(length)
    except (ValueError, TypeError):
        # Fallback: if non-numeric, just return the same (or you can change behavior)
        return max_code


def get_next_service_code_logic():
    """
    Small wrapper to expose next service code via API.
    """
    db = get_db()
    session = db.get_session()

    try:
        next_code = get_next_service_code(session)
        return jsonify({"next_code": next_code}), 200
    finally:
        session.close()


def save_service_logic(data: dict):
    """
    Create or update a service.
    Expected fields:
      - idservice (optional for update)
      - service_code (optional for create: if missing, auto-generated)
      - service_name (required)
      - service_price (required, numeric)
      - service_status (optional: 'active' | 'inactive', default 'active')
    """
    required = ["service_name", "service_price"]
    missing = [f for f in required if not str(data.get(f, "")).strip()]

    if missing:
        return jsonify({
            "error": "Validation failed",
            "missing_fields": missing
        }), 400

    db = get_db()
    session = db.get_session()

    try:
        service_id = data.get("idservice") or data.get("id")

        if service_id:
            # UPDATE
            service = (
                session.query(Service)
                .filter_by(idservice=service_id)
                .first()
            )
            if not service:
                return jsonify({"error": "Service not found"}), 404
        else:
            # CREATE
            # If service_code not provided, auto-generate
            raw_code = (data.get("service_code") or "").strip()
            if not raw_code:
                raw_code = get_next_service_code(session)

            service = Service(
                service_code=raw_code,
                service_name=data["service_name"].strip()
            )
            session.add(service)

        # Common fields
        # Service code is usually immutable, but we allow updating if provided
        service_code = (data.get("service_code") or service.service_code or "").strip()
        if not service_code:
          # Safety fallback
          service_code = get_next_service_code(session)
        service.service_code = service_code

        service.service_name = data["service_name"].strip()

        # Price as Decimal
        try:
            price_str = str(data["service_price"]).strip()
            service.service_price = Decimal(price_str)
        except Exception:
            return jsonify({"error": "service_price must be numeric"}), 400

        # Status: 'active' / 'inactive'
        status = (data.get("service_status") or "active").strip().lower()
        if status not in ("active", "inactive"):
            status = "active"
        service.service_status = status

        session.commit()

        return jsonify({
            "status": "success",
            "idservice": service.idservice,
            "service_code": service.service_code
        }), (201 if not service_id else 200)

    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()


def get_services_logic():
    """
    Return all services as a JSON list.
    """
    db = get_db()
    session = db.get_session()

    try:
        rows = (
            session.query(Service)
            .order_by(Service.idservice)
            .all()
        )

        result = []
        for r in rows:
            result.append({
                "idservice": r.idservice,
                "service_code": r.service_code,
                "service_name": r.service_name,
                "service_price": float(r.service_price) if r.service_price is not None else None,
                "service_status": r.service_status,
                "created_at": r.created_at.isoformat() if r.created_at else None,
                "modified_at": r.modified_at.isoformat() if r.modified_at else None,
            })

        return jsonify(result), 200

    finally:
        session.close()
