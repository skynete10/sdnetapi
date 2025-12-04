from app.connections import get_db
from app.models.users_model import User
import bcrypt
from app.models.settings_model import CurrencySettings
from app.models.settings_model import Settings


def get_users_controller(username=None, mobile=None):
    db = get_db()
    session = db.get_session()

    try:
        query = session.query(User)

        if username:
            query = query.filter(User.username == username)

        if mobile:
            query = query.filter(User.mobile == mobile)

        users = query.all()

        return [
            {
                "idusers": u.idusers,
                "username": u.username,
                "mobile": u.mobile,
                "app_token": u.app_token,
                "created_at": u.created_at.isoformat() if u.created_at else None,
                "modified_at": u.modified_at.isoformat() if u.modified_at else None,
            }
            for u in users
        ]

    finally:
        session.close()


def login_controller(username, password, token=None):
    db = get_db()
    session = db.get_session()

    try:
        # ----- 1) Find user -----
        user = session.query(User).filter(User.username == username).first()
        if not user:
            return None

        # ----- 2) Check password (bcrypt) -----
        if not bcrypt.checkpw(
            password.encode("utf-8"),
            user.password_hash.encode("utf-8"),
        ):
            return None

        # ----- 3) Update token if provided -----
        if token:
            user.app_token = token
            session.commit()

        # ----- 4) Load currency settings (first row or defaults) -----
        cs = session.query(CurrencySettings).first()
        if cs:
            currency_settings = {
                "from_currency": cs.from_currency,
                "to_currency": cs.to_currency,
                "conversion_operator": cs.conversion_operator,
                "curr_rate": float(cs.curr_rate),
            }
        else:
            # Fallback defaults – adjust as you like
            currency_settings = {
                "from_currency": "USD",
                "to_currency": "LBP",
                "conversion_operator": "*",
                "curr_rate": 90000.0,
            }

        # ----- 5) Load generic settings table (title/value) -----
        settings_rows = session.query(Settings).all()
        # return as simple dict: { "wish": "phone...", "another_key": "value", ... }
        settings_dict = {row.title: row.value for row in settings_rows if row.title}

        # ----- 6) Final response -----
        return {
            "idusers": user.idusers,
            "username": user.username,
            "fullname": user.fullname,
            "mobile": user.mobile,
            "app_token": user.app_token,
            "currency_settings": currency_settings,
            "settings": settings_dict,
        }

    finally:
        session.close()