# app/routes/expenses_routes.py

from flask import Blueprint, request

from app.controllers.expenses_controller import (
    list_expenses_logic,
    save_expense_logic,
)

expenses_bp = Blueprint("expenses_bp", __name__)


@expenses_bp.get("/api/expenses")
def api_get_expenses():
    """
    HTTP GET: return all expenses.
    """
    # Controller already returns (json, status_code)
    return list_expenses_logic()


@expenses_bp.post("/api/expenses/saveexpense")
def api_save_expense():
    """
    HTTP POST: create / update an expense.
    """
    payload = request.get_json(silent=True) or {}
    # Controller handles validation, SQLAlchemy errors, and returns proper response
    return save_expense_logic(payload)
