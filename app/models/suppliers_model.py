# app/models/suppliers_model.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Enum,
    MetaData,
    text,
)
from sqlalchemy.orm import declarative_base

# Use the same metadata as the rest of SDNet
sdnet_metadata = MetaData()
SDNetBase = declarative_base(metadata=sdnet_metadata)


class Supplier(SDNetBase):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Supplier fields (parallel to customer)
    supplier_name = Column(String(150), nullable=False)
    contact_person = Column(String(100), nullable=True)
    mobile = Column(String(20), nullable=False, unique=True)
    supplier_code = Column(String(50), nullable=False, unique=True)  # Like username
    email = Column(String(150), nullable=True)
    category = Column(String(50), nullable=True)  # e.g. Hardware, ISP, Maintenance

    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP")
    )


class SupplierAddress(SDNetBase):
    __tablename__ = "supplier_addresses"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Linked by supplier_code (NOT a foreign key, same as customers)
    supplier_code = Column(String(50), nullable=False, unique=True)

    city = Column(String(50), nullable=True)
    village = Column(String(50), nullable=True)
    street = Column(String(100), nullable=True)
    building = Column(String(50), nullable=True)
    floor = Column(String(10), nullable=True)

    type = Column(
        Enum("office", "warehouse", "other", name="supplier_address_type"),
        server_default="office",
        nullable=False
    )

    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )
