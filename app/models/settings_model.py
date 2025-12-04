from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, text
from sqlalchemy.orm import declarative_base

SDNetBase = declarative_base()

class CurrencySettings(SDNetBase):
    __tablename__ = "currency_settings"

    id = Column(Integer, primary_key=True, autoincrement=True)

    from_currency = Column(String(10), nullable=False)     
    to_currency = Column(String(45), nullable=True)       

    conversion_operator = Column(String(1), nullable=False) 
    curr_rate = Column(DECIMAL(18, 4), nullable=False)     

    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )

    def __repr__(self):
        return (
            f"<CurrencySettings id={self.id} "
            f"from={self.from_currency} to={self.to_currency} "
            f"op={self.conversion_operator} rate={self.curr_rate}>"
        )

class Settings(SDNetBase):
    __tablename__ = "settings"

    idsettings = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(45), nullable=True)
    value = Column(String(45), nullable=True)

    def __repr__(self):
        return f"<Settings id={self.idsettings} title={self.title} value={self.value}>"
