from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy import event

from db.base import Base
from model.orderitem import OrderItem
from logger.logger import logger


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


@event.listens_for(Product, 'before_delete')
def set_product_id_on_product_delete(mapper, connection, product):
    logger.info(f"Before deleting Product with ID: {product.id}")
    connection.execute(
        OrderItem.__table__.update()
        .where(OrderItem.product_id == product.id)
        .values(deleted_product_id=product.id)
    )
