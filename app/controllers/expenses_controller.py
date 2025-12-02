# app/controllers/expenses_controller.py

from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List

from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError

from app.connections import get_db
from app.models.expenses_model import Expense


def _parse_expense_date(date_str: str):
    """
    Parse a 'YYYY-MM-DD' date string to a date object.
    Raises ValueError if invalid.
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("expense_date must be in YYYY-MM-DD format")


def save_expense_logic(data: Dict[str, Any]):
    """
    Insert or update an expense.

    Expected payload:
    {
      "id": (optional, for edit),
      "expense_date": "YYYY-MM-DD",
      "category": "string",
      "description": "string",
      "amount": number,
      "notes": "string"
    }
    """
    # ---- validation of required fields ----
    required = ["expense_date", "category", "amount"]
    missing = [f for f in required if not str(data.get(f, "")).strip()]

    if missing:
        return jsonify(
            {
                "error": "Validation failed",
                "missing_fields": missing,
            }
        ), 400

    # parse date
    expense_date_str = str(data.get("expense_date", "")).strip()
    try:
        expense_date = _parse_expense_date(expense_date_str)
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    # parse amount
    try:
        amount_raw = data.get("amount")
        amount = Decimal(str(amount_raw))
    except (InvalidOperation, TypeError):
        return jsonify({"error": "amount must be a valid number"}), 400

    category = str(data.get("category", "")).strip()
    description = str(data.get("description", "")).strip() or None
    notes = str(data.get("notes", "")).strip() or None

    db = get_db()
    session = db.get_session()

    try:
        exp_id = data.get("id")

        if exp_id:
            # ---- update existing ----
            expense = session.query(Expense).get(exp_id)
            if not expense:
                return jsonify({"error": "Expense not found"}), 404
        else:
            # ---- create new ----
            expense = Expense(expense_date=expense_date, category=category)
            session.add(expense)

        # common field assignments (for both create & update)
        expense.expense_date = expense_date
        expense.category = category
        expense.description = description
        expense.amount = amount
        expense.notes = notes

        session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "id": expense.id,
                    "expense_date": expense.expense_date.isoformat()
                    if expense.expense_date
                    else None,
                    "category": expense.category or "",
                    "description": expense.description or "",
                    "amount": float(expense.amount or 0),
                    "notes": expense.notes or "",
                }
            ),
            201 if not exp_id else 200,
        )

    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()


def list_expenses_logic():
    """
    Return all expenses ordered by expense_date desc, id desc as JSON list.
    """
    db = get_db()
    session = db.get_session()

    try:
        q = (
            session.query(Expense)
            .order_by(Expense.expense_date.desc(), Expense.id.desc())
        )
        rows: List[Expense] = q.all()

        result: List[Dict[str, Any]] = []
        for e in rows:
            result.append(
                {
                    "id": e.id,
                    "expense_date": e.expense_date.isoformat()
                    if e.expense_date is not None
                    else None,
                    "category": e.category or "",
                    "description": e.description or "",
                    "amount": float(e.amount or 0),
                    "notes": e.notes or "",
                    "created_at": e.created_at.isoformat()
                    if getattr(e, "created_at", None)
                    else None,
                    "updated_at": e.updated_at.isoformat()
                    if getattr(e, "updated_at", None)
                    else None,
                }
            )

        return jsonify(result), 200

    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()
