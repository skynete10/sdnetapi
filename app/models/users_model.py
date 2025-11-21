from sqlalchemy import Column, Integer, String, DateTime, MetaData, text
from sqlalchemy.orm import declarative_base

sdnet_metadata = MetaData()
SDNetBase = declarative_base(metadata=sdnet_metadata)


class User(SDNetBase):
    __tablename__ = "users"

    idusers = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(45), nullable=False)
    fullname = Column(String(45), nullable=False)
    password_hash = Column(String(255), nullable=False)
    mobile = Column(String(45), nullable=True)
    app_token = Column(String(255), nullable=True)
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )
    modified_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP")
    )
