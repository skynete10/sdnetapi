from app.connections import get_db
from app.models.users_model import User
import bcrypt


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
        user = session.query(User).filter(User.username == username).first()
        if not user:
            return None

        # bcrypt password verification
        if not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
            return None

        # update token if provided
        if token:
            user.app_token = token
            session.commit()

        return {
            "idusers": user.idusers,
            "username": user.username,
            "fullname": user.fullname,
            "mobile": user.mobile,
            "app_token": user.app_token
        }

    finally:
        session.close()