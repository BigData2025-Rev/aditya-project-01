from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.base import Base

class Category(Base):
    __tablename__='category'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    product = relationship('Product', back_populates='categ', cascade='none')
