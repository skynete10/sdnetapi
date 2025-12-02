from flask import Blueprint, request, jsonify

from app.controllers.internet_manager_payment_controller import (
    pay_selected_invoices_controller,
    get_internet_payments_controller,
    clear_payment,
)

internet_manager_payment_bp = Blueprint("internet_manager_payment_bp", __name__)


@internet_manager_payment_bp.post("/api/internet-manager/pay-invoice")
def pay_invoice_route():
    data = request.get_json(silent=True) or {}
    items = data.get("items") or []

    if not isinstance(items, list) or not items:
        return jsonify({"error": "items is required"}), 400

    result = pay_selected_invoices_controller(items)

    if isinstance(result, tuple):
        body, status = result
        return jsonify(body), status

    return jsonify(result), 200


@internet_manager_payment_bp.get("/api/internet-manager/payments")
def get_internet_payments_route():
    """
    Query params:
      - invoice_number: int (required)
      - invoice_month: 'YYYY-MM' (optional)
    """
    invoice_number = request.args.get("invoice_number", type=int)
    invoice_month = request.args.get("invoice_month", type=str)

    result = get_internet_payments_controller(
        invoice_number=invoice_number,
        invoice_month=invoice_month,
    )

    # controller can return list OR (dict, status)
    if isinstance(result, tuple):
        body, status = result
        return jsonify(body), status

    return jsonify(result), 200


@internet_manager_payment_bp.delete("/api/internet-manager/payments/<int:payment_id>")
def clear_payment_route(payment_id: int):
    td, session = clear_payment(payment_id)

    if td is None:
        session.close()
        return jsonify({"error": "Payment not found"}), 404

    try:
        session.commit()
        session.refresh(td)  # refresh from DB after commit

        return jsonify({
            "success": True,
            "id": td.id,
            "invoice_number": td.invoice_number,
            "payment": float(td.payment),
            "net_amount": float(td.net_amount),
        }), 200

    except Exception as exc:
        session.rollback()
        return jsonify({"error": str(exc)}), 500

    finally:
        session.close()
 