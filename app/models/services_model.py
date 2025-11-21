# app/models/services_model.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    DECIMAL,
    DateTime,
    text,
)
from app.connections import SDNetBase


class Service(SDNetBase):
    __tablename__ = "services"

    idservice = Column(Integer, primary_key=True, autoincrement=True)

    service_code = Column(String(50), unique=True, nullable=False)
    service_name = Column(String(100), nullable=False)
    service_price = Column(DECIMAL(10, 2), nullable=False, server_default="0.00")
    service_status = Column(String(10), nullable=False, server_default="active")

    created_at = Column(
        DateTime, server_default=text("CURRENT_TIMESTAMP")
    )
    modified_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )
