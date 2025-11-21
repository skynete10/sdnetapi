from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Enum,
    MetaData,
    text,
    DECIMAL,
)
from sqlalchemy.orm import declarative_base

sdnet_metadata = MetaData()
SDNetBase = declarative_base(metadata=sdnet_metadata)


class Customer(SDNetBase):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(100), nullable=False)
    mobile = Column(String(20), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)

    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP")
    )


class CustomerAddress(SDNetBase):
    __tablename__ = "customer_addresses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)

    city = Column(String(50), nullable=True)
    village = Column(String(50), nullable=True)
    street = Column(String(100), nullable=True)
    building = Column(String(50), nullable=True)
    floor = Column(String(10), nullable=True)

    type = Column(
        Enum("home", "work", "other", name="address_type"),
        server_default="home",
        nullable=False
    )

    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )


class CustomerSubscription(SDNetBase):
    __tablename__ = "customer_subscriptions"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # NO FOREIGN KEYS — now treated as normal text columns
    customer_username = Column(
        String(100),
        nullable=False
    )

    service_code = Column(
        String(50),
        nullable=False
    )

    amount = Column(
        DECIMAL(10, 2),
        nullable=False,
        server_default="0.00",
    )

    billing_date = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    modified_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )
