from sqlalchemy import Integer, String, DECIMAL, DateTime, func, ForeignKey
from sqlalchemy.orm import mapped_column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Account(Base):
    __tablename__ = 'Accounts'

    account_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey('Users.user_id', ondelete="CASCADE"), nullable=False)
    account_type = mapped_column(String(255), nullable=False)
    account_number = mapped_column(String(255), nullable=False, unique=True)
    balance = mapped_column(DECIMAL(10, 2), default=0)
    created_at = mapped_column(DateTime, server_default=func.now())
    updated_at = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
