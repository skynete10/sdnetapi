# app/controllers/customers_controller.py
from flask import request, jsonify
from app.connections import get_db
from app.models.customers_model import Customer, CustomerAddress
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
import os


def get_customers():
    db = get_db()
    session = db.get_session()

    try:
        # LEFT JOIN: return customer even if they have no addresses
        rows = (
            session.query(
                Customer.id,
                Customer.fullname,
                Customer.mobile,
                Customer.username,
                CustomerAddress.city,
                CustomerAddress.village,
                CustomerAddress.street,
                CustomerAddress.building,
            )
            .outerjoin(CustomerAddress, CustomerAddress.username == Customer.username)
            .order_by(Customer.id)
            .all()
        )

        result = [
            {
                "id": r.id,
                "fullname": r.fullname,
                "mobile": r.mobile,
                "username": r.username,
                "city": r.city or "",
                "village": r.village or "",
                "street": r.street or "",
                "building": r.building or "",
            }
            for r in rows
        ]

        return jsonify(result), 200

    finally:
        session.close()


def import_customers_excel():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if not file or not file.filename:
        return jsonify({"error": "Empty filename"}), 400

    filename = (file.filename or "").lower()
    ext = os.path.splitext(filename)[1]

    # ---- Read Excel ----
    try:
        if ext == ".xlsx":
            df = pd.read_excel(file, engine="openpyxl")
        elif ext == ".xls":
            df = pd.read_excel(file, engine="xlrd")
        else:
            return jsonify({"error": f"Unsupported file type: {ext}"}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to read Excel: {e}"}), 400

    # ---- Remove fully empty rows ----
    df = df.dropna(how="all")
    if df.empty:
        return jsonify({"error": "Excel contains no non-empty rows"}), 400

    # ---- Normalize (NaN → "") ----
    df = df.fillna("").astype(str)

    customers = []
    customer_addresses = []

    for _, row in df.iterrows():
        fullname = row.get("Full Name", "").strip()
        mobile = row.get("Mobile", "").strip()
        price = row.get("Price", "").strip()  # not stored in DB here
        username = row.get("Username", "").strip()

        city = row.get("City", "").strip()
        village = row.get("Village", "").strip()
        street = row.get("Street", "").strip()
        building = row.get("Building", "").strip()

        # Skip fully empty or corrupt rows
        if not fullname and not mobile and not username:
            continue

        customers.append(
            {
                "fullname": fullname,
                "mobile": mobile,
                "price": price,
                "username": username,
            }
        )

        customer_addresses.append(
            {
                "username": username,
                "city": city,
                "village": village,
                "street": street,
                "building": building,
            }
        )

    # ---- Insert / update in MySQL (upsert per row) ----
    db = get_db()
    session = db.get_session()

    created_customers = 0
    updated_customers = 0
    created_addresses = 0
    updated_addresses = 0

    try:
        for idx, c in enumerate(customers):
            username = c["username"]
            if not username:
                # cannot map without username, skip
                continue

            # --- UPSERT Customer ---
            customer = (
                session.query(Customer)
                .filter(Customer.username == username)
                .first()
            )

            if customer:
                # Update existing customer
                if c["fullname"]:
                    customer.fullname = c["fullname"]
                if c["mobile"]:
                    customer.mobile = c["mobile"]
                updated_customers += 1
            else:
                # Create new customer
                password_hash = c["mobile"] or "123456"
                customer = Customer(
                    fullname=c["fullname"] or username,
                    mobile=c["mobile"],
                    username=username,
                    password_hash=password_hash,
                )
                session.add(customer)
                created_customers += 1

            # --- UPSERT CustomerAddress for same row ---
            a = customer_addresses[idx]

            addr = (
                session.query(CustomerAddress)
                .filter(CustomerAddress.username == username)
                .first()
            )

            if addr:
                # Update existing address (only overwrite if Excel has value)
                if a["city"]:
                    addr.city = a["city"]
                if a["village"]:
                    addr.village = a["village"]
                if a["street"]:
                    addr.street = a["street"]
                if a["building"]:
                    addr.building = a["building"]
                updated_addresses += 1
            else:
                # Create new address
                addr = CustomerAddress(
                    username=username,
                    city=a["city"] or None,
                    village=a["village"] or None,
                    street=a["street"] or None,
                    building=a["building"] or None,
                    floor=None,
                    type="home",
                )
                session.add(addr)
                created_addresses += 1

        session.commit()

    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

    processed_usernames = sorted(
        {c["username"] for c in customers if c["username"]}
    )

    return (
        jsonify(
            {
                "status": "success",
                "row_count": len(customers),
                "created_customers": created_customers,
                "updated_customers": updated_customers,
                "created_addresses": created_addresses,
                "updated_addresses": updated_addresses,
                "usernames_count": len(processed_usernames),
                "customers": customers,
                "customer_addresses": customer_addresses,
                "usernames": processed_usernames,
            }
        ),
        200,
    )


def save_customer():
    data = request.get_json() or {}
    db = get_db()
    s = db.get_session()

    try:
        customer_id = data.get("id")

        if customer_id:
            # UPDATE
            customer = s.query(Customer).filter_by(id=customer_id).first()
            if not customer:
                return jsonify({"error": "Customer not found"}), 404
        else:
            # CREATE
            customer = Customer(
                username=data["username"],
                mobile=data["mobile"],
                password_hash=data["mobile"] or "123456",
            )
            s.add(customer)

        # Common fields
        customer.fullname = data["fullname"]
        customer.mobile = data["mobile"]
        customer.username = data["username"]

        # Address upsert
        addr = (
            s.query(CustomerAddress)
            .filter_by(username=customer.username)
            .first()
        )
        if not addr:
            addr = CustomerAddress(username=customer.username, type="home")
            s.add(addr)

        addr.city = data.get("city")
        addr.village = data.get("village")
        addr.street = data.get("street")
        addr.building = data.get("building")

        s.commit()
        return jsonify({"status": "success"}), 201 if not customer_id else 200

    except Exception as e:
        s.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        s.close()


def customers_count():
    db = get_db()
    session = db.get_session()
    try:
        total = session.query(Customer).count()
        return jsonify({"total": total}), 200
    finally:
        session.close()
