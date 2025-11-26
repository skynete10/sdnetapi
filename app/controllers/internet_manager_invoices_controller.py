# app/routes/internet_manager_invoices.py

from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, desc, and_

from app.connections import get_db
from app.models.customers_model import Customer
from app.models.transaction_master_model import TransactionMaster

bp = Blueprint("internet_manager_invoices", __name__)

def _payment_to_status_int(payment: str) -> int:
    if payment == "paid":
        return 1
    if payment == "partial":
        return 2
    return 0

def _get_next_invoice_number(s) -> int:
    max_no = s.query(func.max(TransactionMaster.invoice_number)).scalar()
    if max_no is None:
        return 1
    return int(max_no) + 1

def _month_bounds(month_str: str):
    """
    month_str: 'YYYY-MM'
    returns (start_dt, end_dt)
    """
    if not month_str:
        return None, None
    try:
        y, m = month_str.split("-")
        y = int(y); m = int(m)
        start_dt = func.str_to_date(f"{y:04d}-{m:02d}-01", "%Y-%m-%d")
        if m == 12:
            end_dt = func.str_to_date(f"{y+1:04d}-01-01", "%Y-%m-%d")
        else:
            end_dt = func.str_to_date(f"{y:04d}-{m+1:02d}-01", "%Y-%m-%d")
        return start_dt, end_dt
    except:
        return None, None


@bp.post("/api/internet-manager/billing")
def billing_selected():
    db = get_db()
    s = db.get_session()

    try:
        payload = request.get_json(silent=True) or {}

        # ✅ new way
        items = payload.get("items", [])
        # ✅ backward compatibility
        ids = payload.get("ids", [])

        month = (payload.get("month") or "").strip()  # optional 'YYYY-MM'

        if not items and not ids:
            return jsonify({"error": "No items/ids provided"}), 400

        # normalize items -> ids
        if items:
            ids = [int(x.get("id")) for x in items if x.get("id") is not None]

        if not ids:
            return jsonify({"error": "No valid ids provided"}), 400

        customers = s.query(Customer).filter(Customer.id.in_(ids)).all()
        now_dt = func.now()
        start_dt, end_dt = _month_bounds(month)

        item_by_id = {int(x["id"]): x for x in items if x.get("id") is not None}

        inserted = 0
        updated = 0
        assigned_numbers = []

        for c in customers:
            if not c.username:
                continue

            item = item_by_id.get(int(c.id), {})
            sent_invoice_no = item.get("invoice_number")  # may be None
            sent_amount = item.get("amount")

            # fallback amount from customer if not sent
            if sent_amount is None:
                sent_amount = getattr(c, "amount", None)

            # find existing invoice (month scoped if month provided)
            q = s.query(TransactionMaster).filter(
                TransactionMaster.customer_username == c.username
            )
            if start_dt is not None and end_dt is not None:
                q = q.filter(
                    and_(
                        TransactionMaster.invoice_date >= start_dt,
                        TransactionMaster.invoice_date < end_dt
                    )
                )

            existing = q.order_by(desc(TransactionMaster.invoice_date)).first()
            pay_status_int = _payment_to_status_int(getattr(c, "payment", "") or "")

            if existing:
                # ✅ UPDATE existing invoice
                existing.invoiced = 1
                existing.invoice_date = now_dt
                existing.payment_status = pay_status_int

                # if frontend sent invoice_number, prefer it
                if sent_invoice_no:
                    existing.invoice_number = int(sent_invoice_no)

                # save amount if column exists
                if hasattr(existing, "amount"):
                    existing.amount = float(sent_amount or 0)

                invoice_no = int(existing.invoice_number) if existing.invoice_number else 0
                updated += 1
            else:
                # ✅ INSERT new invoice
                invoice_no = int(sent_invoice_no) if sent_invoice_no else _get_next_invoice_number(s)

                tm = TransactionMaster(
                    customer_username=c.username,
                    invoice_number=invoice_no,
                    invoiced=1,
                    invoice_date=now_dt,
                    payment_status=pay_status_int,
                )
                if hasattr(tm, "amount"):
                    tm.amount = float(sent_amount or 0)

                s.add(tm)
                inserted += 1

            # update customer flags if columns exist
            if hasattr(c, "invoiced"):
                c.invoiced = 1
            if hasattr(c, "invoice_number"):
                c.invoice_number = invoice_no

            assigned_numbers.append({
                "customer_username": c.username,
                "invoice_number": invoice_no,
                "amount": float(sent_amount or 0)
            })

        s.commit()
        return jsonify({
            "success": True,
            "inserted": inserted,
            "updated": updated,
            "assigned": assigned_numbers
        }), 200

    except SQLAlchemyError as e:
        s.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        s.close()


@bp.post("/api/internet-manager/cancel-invoice")
def cancel_invoice_selected():
    db = get_db()
    s = db.get_session()

    try:
        payload = request.get_json(silent=True) or {}
        ids = payload.get("ids", [])
        month = (payload.get("month") or "").strip()  # optional 'YYYY-MM'

        if not ids:
            return jsonify({"error": "No ids provided"}), 400

        customers = s.query(Customer).filter(Customer.id.in_(ids)).all()
        now_dt = func.now()

        start_dt, end_dt = _month_bounds(month)

        inserted = 0
        updated = 0
        affected_numbers = []

        for c in customers:
            if not c.username:
                continue

            q = s.query(TransactionMaster).filter(
                TransactionMaster.customer_username == c.username
            )
            if start_dt is not None and end_dt is not None:
                q = q.filter(
                    and_(
                        TransactionMaster.invoice_date >= start_dt,
                        TransactionMaster.invoice_date < end_dt
                    )
                )

            existing = q.order_by(desc(TransactionMaster.invoice_date)).first()
            pay_status_int = _payment_to_status_int(getattr(c, "payment", "") or "")

            if existing and existing.invoice_number:
                # ✅ Update existing record to cancel (keep invoice_number)
                existing.invoiced = 0
                existing.invoice_date = now_dt
                existing.payment_status = pay_status_int

                invoice_no = int(existing.invoice_number)
                updated += 1
            else:
                # If no existing invoice, create a cancel record with NEW number
                invoice_no = _get_next_invoice_number(s)

                tm = TransactionMaster(
                    customer_username=c.username,
                    invoice_number=invoice_no,
                    invoiced=0,
                    invoice_date=now_dt,
                    payment_status=pay_status_int,
                )
                s.add(tm)
                inserted += 1

            if hasattr(c, "invoiced"):
                c.invoiced = 0
            if hasattr(c, "invoice_number"):
                c.invoice_number = invoice_no

            affected_numbers.append({
                "customer_username": c.username,
                "invoice_number": invoice_no,
                "invoiced": 0
            })

        s.commit()
        return jsonify({
            "success": True,
            "inserted": inserted,
            "updated": updated,
            "affected": affected_numbers
        }), 200

    except SQLAlchemyError as e:
        s.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        s.close()


@bp.get("/api/internet-manager/invoices")
def get_invoices_for_month():
    db = get_db()
    s = db.get_session()

    try:
        month = (request.args.get("month") or "").strip()
        if not month or len(month) != 7:
            return jsonify([]), 200

        start_date = f"{month}-01"
        year, mon = month.split("-")
        year = int(year)
        mon = int(mon)
        if mon == 12:
            end_date = f"{year+1}-01-01"
        else:
            end_date = f"{year}-{str(mon+1).zfill(2)}-01"

        subq = (
            s.query(
                TransactionMaster.customer_username.label("cu"),
                func.max(TransactionMaster.invoice_number).label("max_no"),
            )
            .filter(
                and_(
                    TransactionMaster.invoice_date >= start_date,
                    TransactionMaster.invoice_date < end_date,
                    TransactionMaster.customer_username.isnot(None),
                )
            )
            .group_by(TransactionMaster.customer_username)
            .subquery()
        )

        rows = (
            s.query(
                TransactionMaster.customer_username,
                TransactionMaster.invoice_number,
                TransactionMaster.invoiced,
            )
            .join(
                subq,
                and_(
                    TransactionMaster.customer_username == subq.c.cu,
                    TransactionMaster.invoice_number == subq.c.max_no,
                ),
            )
            .all()
        )

        result = [
            {
                "customer_username": r.customer_username,
                "invoice_number": int(r.invoice_number) if r.invoice_number is not None else None,
                "invoiced": 1 if int(r.invoiced or 0) == 1 else 0,
            }
            for r in rows
        ]

        return jsonify(result), 200

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

    finally:
        s.close()
