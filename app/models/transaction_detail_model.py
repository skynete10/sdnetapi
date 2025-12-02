from sqlalchemy import Column, Integer, String, Date, DateTime, DECIMAL, text
from app.connections import SDNetBase


class TransactionDetail(SDNetBase):
    __tablename__ = "transaction_detail"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    invoice_number = Column(
        String(50),
        nullable=False,
        index=True
    )

    payment_date = Column(
        Date,
        nullable=False
    )

    payment = Column(
        DECIMAL(12, 2),
        nullable=False
    )
    
    net_amount = Column(
        DECIMAL(12, 2),
        nullable=False
    )

    currency = Column(
        String(10),
        nullable=False
    )

    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )

    modified_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP")
    )


    def clear_payment(self):
      total = (self.payment or 0) + (self.net_amount or 0)
      self.payment = 0
      self.net_amount = total
