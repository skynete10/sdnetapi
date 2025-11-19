from flask import jsonify, request
from app.connections import get_db
from app.models.settings_model import CurrencySettings

def get_currency_settings():
    """
    GET /api/settings/currency
    Optional query param: ?default_currency=USD or LBP

    - If default_currency provided: load settings for that currency.
      If not found, return sensible defaults for that currency.
    - If not provided: return the first row or global defaults.
    """
    db = get_db()
    session = db.get_session()

    try:
        requested_currency = request.args.get("default_currency")

        # ---- Case 1: specific currency requested ----
        if requested_currency:
            row = (
                session.query(CurrencySettings)
                .filter_by(default_currency=requested_currency)
                .first()
            )

            if row:
                return jsonify({
                    "default_currency": row.default_currency,
                    "conversion_operator": row.conversion_operator,
                    "curr_rate": float(row.curr_rate),
                }), 200

            # If no row exists for that currency, return defaults for it
            # adjust defaults as you like
            if requested_currency == "USD":
                default_operator = "*"
                default_rate = 90000.0    # e.g. 1 USD * 90000 = LBP
            else:  # "LBP" or anything else
                default_operator = "/"
                default_rate = 1 / 90000.0

            return jsonify({
                "default_currency": requested_currency,
                "conversion_operator": default_operator,
                "curr_rate": default_rate,
            }), 200

        # ---- Case 2: no specific currency → return first row or global defaults ----
        row = session.query(CurrencySettings).first()
        if row:
            return jsonify({
                "default_currency": row.default_currency,
                "conversion_operator": row.conversion_operator,
                "curr_rate": float(row.curr_rate),
            }), 200

        # No rows at all → system defaults
        return jsonify({
            "default_currency": "LBP",
            "conversion_operator": "*",
            "curr_rate": 90000.0,
        }), 200

    finally:
        session.close()


def save_currency_settings():
    data = request.get_json()

    default_currency = data.get("default_currency")
    conversion_operator = data.get("conversion_operator")
    curr_rate = data.get("curr_rate")

    if not default_currency or not conversion_operator or curr_rate is None:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        db = get_db()
        session = db.get_session()

        # --- Check if currency already exists ---
        existing = (
            session.query(CurrencySettings)
            .filter_by(default_currency=default_currency)
            .first()
        )

        if existing:
            # --- UPDATE existing ---
            existing.conversion_operator = conversion_operator
            existing.curr_rate = curr_rate
        else:
            # --- INSERT new ---
            new_record = CurrencySettings(
                default_currency=default_currency,
                conversion_operator=conversion_operator,
                curr_rate=curr_rate,
            )
            session.add(new_record)

        session.commit()
        session.close()

        return jsonify({"status": "success"}), 200

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
