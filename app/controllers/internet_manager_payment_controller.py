# app/routes/internet_manager_payment.py

from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, desc, and_
from app.connections import get_db
from datetime import datetime
from typing import List, Dict, Tuple, Union
from app.models.customers_model import Customer
from typing import Dict, Tuple, Union, List, Optional
from app.models.transaction_detail_model import TransactionDetail
from datetime import date

bp = Blueprint("internet_manager_payment", __name__)


def pay_selected_invoices_controller(
    items: List[Dict]
) -> Union[Dict, Tuple[Dict, int]]:
    """
    items: [
      {
        "invoice_number": 123,
        "payment_date": "2025-11-26",   # yyyy-mm-dd
        "amount": 20.0,                 # invoice total
        "payment": 20.0,                # amount paid now
        "net_amount": amount - payment, # remaining after this payment (optional)
        "currency": "USD"
      },
      ...
    ]
    """
    db = get_db()
    session = db.get_session()

    try:
        saved_count = 0

        for item in items:
            invoice_number = item.get("invoice_number")
            if not invoice_number:
                continue

            # --- payment_date ---
            payment_date_str = item.get("payment_date")
            try:
                if payment_date_str:
                    payment_date = datetime.strptime(payment_date_str, "%Y-%m-%d").date()
                else:
                    payment_date = datetime.utcnow().date()
            except ValueError:
                payment_date = datetime.utcnow().date()

            # --- monetary fields ---
            try:
                amount = float(item.get("payment", 0) or 0)
            except (TypeError, ValueError):
                amount = 0.0

            try:
                payment = float(item.get("payment", 0) or 0)
            except (TypeError, ValueError):
                payment = 0.0

            # if net_amount not sent, compute it as amount - payment
            net_raw = item.get("net_amount", None)
            if net_raw is None:
                net_amount = amount - payment
            else:
                try:
                    net_amount = float(net_raw)
                except (TypeError, ValueError):
                    net_amount = amount - payment

            currency = (item.get("currency") or "USD").upper()

            td = TransactionDetail(
                invoice_number=str(invoice_number),
                payment_date=payment_date,
                payment=payment,
                net_amount=net_amount,
                currency=currency,
            )
            session.add(td)
            saved_count += 1

        session.commit()
        return {"success": True, "saved": saved_count}
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        return {"success": False, "error": str(e)}, 500
    finally:
        session.close()


def get_internet_payments_controller(
    invoice_number: int,
    invoice_month: Optional[str] = None,
) -> Union[List[Dict], Tuple[Dict, int]]:
    """
    Fetch payments for a given invoice.
    - invoice_number: required
    - invoice_month: 'YYYY-MM' or None (if None => all months)

    Returns:
      On success: [ { ... }, ... ]
      On error: ({ "error": "..." }, 500) or ({"error": "...invalid..."}, 400)
    """
    db = get_db()
    session = db.get_session()

    try:
        if not invoice_number:
            return {"error": "invoice_number is required"}, 400

        q = session.query(TransactionDetail).filter(
            TransactionDetail.invoice_number == str(invoice_number)
        )

        # optional filter by month: YYYY-MM (same as filterDate/draftFilterDate)
        if invoice_month:
            try:
                year_str, month_str = invoice_month.split("-")
                year = int(year_str)
                month = int(month_str)

                first_day = date(year, month, 1)
                if month == 12:
                    next_month_first = date(year + 1, 1, 1)
                else:
                    next_month_first = date(year, month + 1, 1)

                q = q.filter(
                    and_(
                        TransactionDetail.payment_date >= first_day,
                        TransactionDetail.payment_date < next_month_first,
                    )
                )
            except ValueError:
                return {"error": "invoice_month must be in YYYY-MM format"}, 400

        q = q.order_by(TransactionDetail.payment_date.desc())

        rows = q.all()

        data: List[Dict] = [
            {
                "id": r.id,  # or r.idtransaction_detail
                "payment_date": (
                    r.payment_date.isoformat() if r.payment_date else None
                ),
                "amount": float(r.payment or 0),
                "method": getattr(r, "payment_method", None)
                or getattr(r, "method", None)
                or "",
            }
            for r in rows
        ]

        return data

    except SQLAlchemyError as e:
        session.rollback()
        return {"error": str(e)}, 500
    finally:
        session.close()