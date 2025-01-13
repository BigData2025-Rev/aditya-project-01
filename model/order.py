from datetime import datetime
import json
import uuid
import enum
from logger.logger import logger

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, BINARY
from db.base import Base

from sqlalchemy.orm import relationship

class OrderStatus(enum.Enum):
    pending = 'pending'
    completed = 'completed'
    shipped = 'shipped'
    delivered = 'delivered'
    canceled = 'canceled'
    returned = 'returned'

class Order(Base):
    __tablename__="order"

    id = Column(Integer, primary_key=True)
    ordered_by = Column(BINARY(16), ForeignKey('user.id', ondelete='SET NULL'), nullable=True)
    deleted_ordered_by = Column(BINARY(16), nullable=True)
    status = Column(String(50), nullable=False, default=OrderStatus.pending.value)
    created_at = Column(DateTime, default=datetime.now())
    total = Column(Float)

    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    user = relationship("User", back_populates="orders")

    @property
    def status_enum(self):
        return OrderStatus[self.status.lower()]

    @staticmethod
    def get_json_values(orders):
        response = []
        for order in orders:
            order_dict = {}
            order_dict['order_id'] = order.id
            order_dict['order_created'] = str(order.created_at)
            order_dict['order_status'] = order.status
            order_dict['ordered_by'] = None
            if order.ordered_by:
                order_dict['ordered_by'] = str(uuid.UUID(bytes=order.ordered_by))
            total = 0.0
            if len(order.order_items) > 0:
                order_dict['items'] = []
                for item in order.order_items:
                    if item and item.product:
                        product = {}
                        total += item.subtotal
                        product['product_name'] = item.product.name
                        product['product_image'] = item.product.image
                        product['product_price'] = item.product.price
                        product['product_quantity'] = item.quantity
                        product['stock_quantity'] = item.product.stock_quantity
                        order_dict['items'].append(json.dumps(product))
            order_dict['total_amount'] = f"{total:.2f}"
            logger.info(order_dict)
            response.append(json.dumps(order_dict))
        return response

    @staticmethod
    def get_json_value(order):
        order_dict = {}
        order_dict['order_id'] = order.id
        order_dict['order_created'] = str(order.created_at)
        order_dict['total_amount'] = f"{order.total:.2f}"
        order_dict['order_status'] = order.status
        order_dict['ordered_by'] = str(uuid.UUID(bytes=order.ordered_by))
        order_dict['order_items'] = order.order_items
        return order_dict
