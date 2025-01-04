import datetime

from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from db.base import Base

from model.order import Order

class OrderItem(Base):
    __tablename__='order_item'

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    unitprice = Column(Float)
    subtotal = Column(Float, default=quantity*unitprice)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)

    order = relationship('Order', back_populates='order_items')
    product = relationship('Product', back_populates='order_item')
