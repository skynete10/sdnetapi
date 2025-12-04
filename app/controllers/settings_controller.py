from flask import jsonify, request
from app.connections import get_db
from app.models.settings_model import CurrencySettings,Settings


def get_currency_settings():
    """
    GET /api/settings/currency
    Optional query params:
      - from_currency=USD|LBP
      - to_currency=USD|LBP

    - If from_currency & to_currency are provided:
        → load settings for that currency pair.
        → If not found, return sensible defaults for that pair.
    - If not provided:
        → return the first row in the table, or global defaults.
    """
    db = get_db()
    session = db.get_session()

    try:
        from_currency = request.args.get("from_currency")
        to_currency = request.args.get("to_currency")

        # ---- Case 1: specific pair requested ----
        if from_currency and to_currency:
            row = (
                session.query(CurrencySettings)
                .filter_by(from_currency=from_currency, to_currency=to_currency)
                .first()
            )

            if row:
                return jsonify({
                    "from_currency": row.from_currency,
                    "to_currency": row.to_currency,
                    "conversion_operator": row.conversion_operator,
                    "curr_rate": float(row.curr_rate),
                }), 200

            # ---- No row exists for that pair → return sensible defaults ----
            # Adjust these defaults as you prefer for your app.
            if from_currency == "USD" and to_currency == "LBP":
                default_operator = "*"
                default_rate = 90000.0
            elif from_currency == "LBP" and to_currency == "USD":
                default_operator = "/"
                default_rate = 1 / 90000.0
            else:
                # Fallback for any other pair
                default_operator = "*"
                default_rate = 1.0

            return jsonify({
                "from_currency": from_currency,
                "to_currency": to_currency,
                "conversion_operator": default_operator,
                "curr_rate": default_rate,
            }), 200

        # ---- Case 2: no specific pair → return first row or global defaults ----
        row = session.query(CurrencySettings).first()
        if row:
            return jsonify({
                "from_currency": row.from_currency,
                "to_currency": row.to_currency,
                "conversion_operator": row.conversion_operator,
                "curr_rate": float(row.curr_rate),
            }), 200

        # No rows at all → system defaults (e.g. USD → LBP)
        return jsonify({
            "from_currency": "USD",
            "to_currency": "LBP",
            "conversion_operator": "*",
            "curr_rate": 90000.0,
        }), 200

    finally:
        session.close()


def save_currency_settings():
    """
    POST /api/settings/currency
    JSON body:
    {
      "from_currency": "USD",
      "to_currency": "LBP",
      "conversion_operator": "*",
      "curr_rate": 90000
    }
    """
    data = request.get_json() or {}

    from_currency = data.get("from_currency")
    to_currency = data.get("to_currency")
    conversion_operator = data.get("conversion_operator")
    curr_rate = data.get("curr_rate")

    # Basic validation
    if not from_currency or not to_currency or not conversion_operator or curr_rate is None:
        return jsonify({"error": "Missing required fields"}), 400

    db = get_db()
    session = db.get_session()

    try:
        # --- Check if this from→to pair already exists ---
        existing = (
            session.query(CurrencySettings)
            .filter_by(from_currency=from_currency, to_currency=to_currency)
            .first()
        )

        if existing:
            # --- UPDATE existing ---
            existing.conversion_operator = conversion_operator
            existing.curr_rate = curr_rate
        else:
            # --- INSERT new ---
            new_record = CurrencySettings(
                from_currency=from_currency,
                to_currency=to_currency,
                conversion_operator=conversion_operator,
                curr_rate=curr_rate,
            )
            session.add(new_record)

        session.commit()
        return jsonify({"status": "success"}), 200

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()

def get_wish_number():
    """
    GET /api/settings/wish

    Returns:
    {
      "title": "wish",
      "number": "xxxxxxxxxx"   # or null if not set
    }
    """
    db = get_db()
    session = db.get_session()

    try:
        row = session.query(Settings).filter_by(title="wish").first()

        if row:
            return jsonify({
                "title": "wish",
                "number": row.value,
            }), 200

        # Not set yet
        return jsonify({
            "title": "wish",
            "number": None,
        }), 200

    finally:
        session.close()


def save_wish_number():
    """
    POST /api/settings/wish

    JSON body:
    {
      "number": "xxxxxxxxxx"
    }

    Saves/updates the Wish Money phone number in the `settings` table
    with title='wish'.
    """
    data = request.get_json() or {}
    number = data.get("number") or data.get("wish_money_phone")

    if not number:
        return jsonify({"error": "Wish Money phone number is required."}), 400

    db = get_db()
    session = db.get_session()

    try:
        row = session.query(Settings).filter_by(title="wish").first()

        if row:
            row.value = number
        else:
            row = Settings(title="wish", value=number)
            session.add(row)

        session.commit()

        return jsonify({
            "status": "success",
            "title": "wish",
            "number": number,
        }), 200

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()