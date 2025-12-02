from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError

from app.connections import get_db
from app.models.customers_model import Customer,CustomerAddress,CustomerSubscription 


def get_internet_customers_logic():
    db = get_db()
    s = db.get_session()

    try:
        rows = (
            s.query(
                Customer.id,
                Customer.username,
                Customer.fullname,
                Customer.customer_status,
                Customer.wish,
                CustomerAddress.city,
                CustomerAddress.village,
                Customer.due_date if hasattr(Customer, "due_date") else None,
                Customer.amount if hasattr(Customer, "amount") else None,
                Customer.invoiced if hasattr(Customer, "invoiced") else None,
                Customer.payment if hasattr(Customer, "payment") else None,
                Customer.status if hasattr(Customer, "status") else None,
            )
            .outerjoin(
                CustomerAddress,
                CustomerAddress.username == Customer.username
            )
            .order_by(Customer.fullname, Customer.username)
            .all()
        )

        customerSubsc_array = {}

        sub_rows = (
         s.query(
        CustomerSubscription.customer_username,
        CustomerSubscription.billing_date,
        CustomerSubscription.amount
        )
        .filter(CustomerSubscription.customer_username.isnot(None))
        .order_by(
          CustomerSubscription.customer_username.asc(),
          CustomerSubscription.billing_date.desc()
        )
        .all()
        )

        for u, bd, amt in sub_rows:
          if u and u not in customerSubsc_array:
            customerSubsc_array[u] = {
              "billing_date": bd.isoformat() if bd else None,
              "amount": float(amt or 0),
            }

        result = []
        for r in rows:
            due_date_val = getattr(r, "due_date", None)
            amount_val = getattr(r, "amount", None)
            invoiced_val = getattr(r, "invoiced", None)
            payment_val = getattr(r, "payment", None)
            status_val = getattr(r, "status", None)

            result.append({
                "id": r.id,
                "username": r.username or "",
                "fullname": r.fullname or "",
                "customer_status": r.customer_status,
                "wish": r.wish,
                "city": r.city or "",
                "village": r.village or "",
                "due_date": customerSubsc_array.get(r.username, {}).get("billing_date"),
                "amount": customerSubsc_array.get(r.username, {}).get("amount"),
                "invoiced": bool(invoiced_val or False),
                "payment": payment_val if payment_val in ("paid", "unpaid", "partial") else "unpaid",
                "status": status_val if status_val in ("active", "stopped") else "active",
            })

        return jsonify(result), 200

    except SQLAlchemyError as e:
        s.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        s.close()
