from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from db.base import Base


class Product(Base):
    __tablename__='product'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    image = Column(String(255), nullable=True)
    rating = Column(Float, nullable=True)
    stock_quantity = Column(Integer, default=0)
    no_of_ratings = Column(Integer, nullable=True)
    category_id = Column(Integer, ForeignKey('category.id', ondelete='set NULL'), nullable=True)
    price = Column(Float, nullable=False)

    order_item = relationship('OrderItem', back_populates='product')
    categ = relationship('Category', back_populates='product')
    
