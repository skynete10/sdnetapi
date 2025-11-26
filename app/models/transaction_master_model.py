from sqlalchemy import Column, BigInteger, String, DateTime, SmallInteger, func,DECIMAL
from app.connections import SDNetBase

class TransactionMaster(SDNetBase):
    __tablename__ = "transaction_master"

    idtransaction_master = Column(BigInteger, primary_key=True, autoincrement=True)
    customer_username = Column(String(45))
    invoice_number = Column(BigInteger, unique=True)
    invoiced = Column(SmallInteger, server_default="0")
    invoice_date = Column(DateTime)
    payment_status = Column(SmallInteger, server_default="0")
    amount = Column(DECIMAL(19, 9), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
