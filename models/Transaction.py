from sqlalchemy import Integer, String, DECIMAL, Enum, DateTime, ForeignKey, func
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'Transactions'

    transaction_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    from_account_id = mapped_column(Integer, ForeignKey('Accounts.account_id', ondelete='CASCADE'))
    to_account_id = mapped_column(Integer, ForeignKey('Accounts.account_id', ondelete='CASCADE'))
    amount = mapped_column(DECIMAL(10, 2), nullable=False)
    transaction_type = mapped_column(Enum('DEPOSIT', 'WITHDRAWAL', 'TRANSFER', name='transaction_type_enum'), nullable=False)
    description = mapped_column(String(255))
    created_at = mapped_column(DateTime, server_default=func.now())
    from_account = relationship("Account", foreign_keys=[from_account_id])
    to_account = relationship("Account", foreign_keys=[to_account_id])
