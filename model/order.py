from datetime import datetime
import json
import uuid
import enum

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
    ordered_by = Column(BINARY(16), ForeignKey('user.id'), nullable=False)
    status = Column(String(50), nullable=False, default=OrderStatus.pending.value)
    created_at = Column(DateTime, default=datetime.now())
    total = Column(Float)

    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    user = relationship("User", back_populates="order")

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
            order_dict['total_amount'] = f"{order.total:.2f}"
            order_dict['order_status'] = order.status
            order_dict['ordered_by'] = str(uuid.UUID(bytes=order.ordered_by))
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
