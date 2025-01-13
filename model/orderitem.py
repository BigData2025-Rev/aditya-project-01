import datetime

from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from db.base import Base


class OrderItem(Base):
    __tablename__='order_item'

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    unitprice = Column(Float)

    order_id = Column(Integer, ForeignKey('order.id', ondelete='SET NULL'), nullable=True)
    deleted_order_id=Column(Integer, nullable=True)
    product_id = Column(Integer, ForeignKey('product.id', ondelete='SET NULL'), nullable=True)
    deleted_product_id = Column(Integer, nullable=True)

    order = relationship('Order', back_populates='order_items')
    product = relationship('Product', back_populates='order_item')

    @property
    def subtotal(self):
        return self.quantity * self.unitprice
