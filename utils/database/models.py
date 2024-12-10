# utils/database/functions/models.py
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String,
    DateTime,
    Boolean,
)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, unique=True)
    username = Column(String(32), nullable=True)
    full_name = Column(String(128), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    referrer_id = Column(BigInteger, nullable=True)
    ref_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"User(id={self.id}, user_id={self.user_id}, username={self.username})"
