from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    DECIMAL,
    Text,
    text,
)
from app.connections import SDNetBase  # adjust if your base is elsewhere


class Expense(SDNetBase):
    __tablename__ = "expenses"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    expense_date = Column(
        Date,
        nullable=False,
        index=True
    )

    category = Column(
        String(50),
        nullable=False,
        index=True
    )

    description = Column(
        String(255),
        nullable=True
    )

    amount = Column(
        DECIMAL(12, 2),
        nullable=False
    )

    notes = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )

    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP")
    )
