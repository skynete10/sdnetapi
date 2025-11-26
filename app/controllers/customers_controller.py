# app/controllers/customers_controller.py
from flask import request, jsonify
from app.connections import get_db
from app.models.customers_model import Customer, CustomerAddress,CustomerSubscription
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from decimal import Decimal,InvalidOperation
import pandas as pd
from app.models.services_model import Service
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
                Customer.customer_status,
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
                "customer_status": r.customer_status,
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

    # We will also keep the raw price per row (string) for later
    row_prices = []

    for _, row in df.iterrows():
        fullname = row.get("Full Name", "").strip()
        mobile = row.get("Mobile", "").strip()
        price_raw = row.get("Price", "").strip()
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
                "price": price_raw,  # keep original string for response
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

        row_prices.append(price_raw)

    # ---- Insert / update in MySQL (upsert per row) ----
    db = get_db()
    session = db.get_session()

    created_customers = 0
    updated_customers = 0
    created_addresses = 0
    updated_addresses = 0

    created_services = 0
    reused_services = 0
    created_subscriptions = 0
    updated_subscriptions = 0

    try:
        # ----- Prepare Service code generation -----
        # max existing service_code (like "000123")
        max_code = session.query(func.max(Service.service_code)).scalar()
        if max_code is None:
            next_service_num = 1
        else:
            try:
                next_service_num = int(max_code) + 1
            except ValueError:
                # if existing codes are weird, restart
                next_service_num = 1

        # cache: price_decimal -> Service instance
        service_cache = {}

        def get_or_create_service_for_price(price_decimal: Decimal) -> Service:
            nonlocal next_service_num, created_services, reused_services

            if price_decimal in service_cache:
                reused_services += 1
                return service_cache[price_decimal]

            # Check in DB first (maybe exists from previous imports)
            existing = (
                session.query(Service)
                .filter(Service.service_price == price_decimal)
                .first()
            )
            if existing:
                service_cache[price_decimal] = existing
                reused_services += 1
                return existing

            # Create new Service with auto code/name like 000001
            code_str = f"{next_service_num:06d}"
            next_service_num += 1

            new_service = Service(
                service_code=code_str,
                service_name=code_str,
                service_price=price_decimal,
                service_currency="USD",
                service_status="1",  # as requested
            )
            session.add(new_service)
            created_services += 1
            service_cache[price_decimal] = new_service
            return new_service

        # ----- Loop rows and upsert everything -----
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
                if c["fullname"]:
                    customer.fullname = c["fullname"]
                if c["mobile"]:
                    customer.mobile = c["mobile"]
                updated_customers += 1
            else:
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

            # --- SERVICE + SUBSCRIPTION for this row (price) ---
            price_str = row_prices[idx].strip()
            if not price_str:
                continue  # no price = no subscription

            # clean common formatting, e.g. "25,000" -> "25000"
            price_str_clean = price_str.replace(",", "")

            try:
                price_decimal = Decimal(price_str_clean)
            except InvalidOperation:
                # invalid number, skip subscription for this row
                continue

            # Get or create Service for this price
            service = get_or_create_service_for_price(price_decimal)

            # Upsert CustomerSubscription for (username, service_code)
            sub = (
                session.query(CustomerSubscription)
                .filter(
                    CustomerSubscription.customer_username == username,
                    CustomerSubscription.service_code == service.service_code,
                )
                .first()
            )

            if sub:
                sub.amount = price_decimal
                updated_subscriptions += 1
            else:
                sub = CustomerSubscription(
                    customer_username=username,
                    service_code=service.service_code,
                    amount=price_decimal,
                    emp_manager="import_excel",  # or use current user if you have it
                    # billing_date -> DB default (CURRENT_TIMESTAMP)
                    # subscription_status -> DB default ("0")
                )
                session.add(sub)
                created_subscriptions += 1

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
                "created_services": created_services,
                "reused_services": reused_services,
                "created_subscriptions": created_subscriptions,
                "updated_subscriptions": updated_subscriptions,
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


def update_customer_status():
    data = request.get_json() or {}
    customer_id = data.get("id")
    status_str = (data.get("status") or "").strip().lower()

    if not customer_id:
        return jsonify({"error": "Missing customer id"}), 400

    if status_str not in ("active", "inactive"):
        return jsonify({"error": "Invalid status, must be 'active' or 'inactive'"}), 400

    # map to tinyint: 1 = active, 0 = inactive
    new_status = 1 if status_str == "active" else 0

    db = get_db()
    s = db.get_session()

    try:
        customer = s.query(Customer).filter_by(id=customer_id).first()
        if not customer:
            return jsonify({"error": "Customer not found"}), 404

        # make sure this column exists in your model:
        # customer_status = Column(SmallInteger, nullable=False, server_default="1")
        customer.customer_status = new_status

        s.commit()
        return jsonify(
            {
                "status": "success",
                "id": customer.id,
                "customer_status": customer.customer_status,
            }
        ), 200

    except Exception as e:
        s.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        s.close()

