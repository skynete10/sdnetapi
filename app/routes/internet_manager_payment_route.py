from flask import Blueprint, request, jsonify

from app.controllers.internet_manager_payment_controller import (
    pay_selected_invoices_controller,
    get_internet_payments_controller,
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
 