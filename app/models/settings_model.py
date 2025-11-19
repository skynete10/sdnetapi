from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, text
from sqlalchemy.orm import declarative_base

SDNetBase = declarative_base()

class CurrencySettings(SDNetBase):
    __tablename__ = "currency_settings"

    id = Column(Integer, primary_key=True, autoincrement=True)

    default_currency = Column(String(10), nullable=False)  # "USD" / "LBP"
    conversion_operator = Column(String(1), nullable=False)  # "*" or "/"
    curr_rate = Column(DECIMAL(18, 4), nullable=False)

    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP")
    )
