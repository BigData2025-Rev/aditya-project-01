from datetime import datetime

import bcrypt
import base64
import uuid
import enum

from logger.logger import logger
from sqlalchemy import Column, Integer, String, DateTime, BINARY, LargeBinary
from sqlalchemy.orm import relationship
from db.base import Base


class Role(enum.Enum):
    admin = 'admin'
    user = 'user'


class User(Base):
    __tablename__="user"

    id = Column(BINARY(16), primary_key=True, default=lambda : uuid.uuid4().bytes)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    role = Column(String(20), nullable=False, default=Role.user.value)
    password_hash = Column(String(100), nullable=False)
    country = Column(String(50))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    order = relationship('Order', back_populates='user', cascade='all, delete-orphan')

    def set_password(self, password):
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        self.password_hash = hashed_password.decode('utf-8')

    def check_password(self, password):
        password_bytes = password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, self.password_hash.encode('utf-8'))

    def __repr__(self):
        return f"User(id: {uuid.UUID(bytes=self.id)}, name: {self.username}, email: {self.email}, country: {self.country}, created_at: {self.created_at})"

    @property
    def role_enum(self):
        return Role[self.role.lower()]
