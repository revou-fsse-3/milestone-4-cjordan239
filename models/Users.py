from models.base import Base
from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import mapped_column
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin
import bcrypt

class User(Base, UserMixin):
    __tablename__ = 'Users'

    user_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    username = mapped_column(String(100), nullable=False, unique=True)
    email = mapped_column(String(100), nullable=False, unique=True)
    password = mapped_column(String(255), nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def get_id(self):
        return str(self.user_id)
    
    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

