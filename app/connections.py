from app.engine import MySQLConnection
from app.models.users_model import SDNetBase

_db = None

def get_db():
    global _db
    if _db is None:
        _db = MySQLConnection(prefix="DB", model_base=SDNetBase)
    return _db
