from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

class MySQLConnection:
    def __init__(self, prefix=None, model_base=None):
        if prefix:
            user_var = f"{prefix}_USER"
            pass_var = f"{prefix}_PASSWORD"
            host_var = f"{prefix}_HOST"
            port_var = f"{prefix}_PORT"
            name_var = f"{prefix}_DB"
        else:
            user_var = "DB_USER"
            pass_var = "DB_PASSWORD"
            host_var = "DB_HOST"
            port_var = "DB_PORT"
            name_var = "DB_NAME"

        self.DB_USER = os.getenv(user_var)
        self.DB_PASSWORD = os.getenv(pass_var)
        self.DB_HOST = os.getenv(host_var)
        self.DB_PORT = os.getenv(port_var, "3306")
        self.DB_NAME = os.getenv(name_var)

        if not all([self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_NAME]):
            raise ValueError("Missing environment variables for MySQL connection")

        self.master_engine = create_engine(
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}",
            echo=False
        )

        with self.master_engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{self.DB_NAME}`"))
            conn.commit()

        self.engine = create_engine(
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}",
            echo=False
        )

        self.SessionLocal = scoped_session(sessionmaker(bind=self.engine))

        if model_base is not None:
            model_base.metadata.create_all(self.engine)

    def get_session(self):
        return self.SessionLocal()

    def close_session(self):
        self.SessionLocal.remove()
