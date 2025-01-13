from service.basehandler import BaseHandler
import json
import uuid

from db.session import session as Db
from logger.logger import logger

from model.order import Order, OrderStatus
from model.orderitem import OrderItem
from model.product import Product
from sqlalchemy import or_
from model.user import User
from utils.decorators.useraccess import access_token_required
from utils.decorators.request import json_required

class RemoveOrder(BaseHandler):
    @access_token_required
    def post(self, order_id):
        with Db() as session:
            try:
                order = session.query(Order).filter(Order.id==order_id).first()
                session.delete(order)
                session.commit()
            except Exception as e:
                logger.info(f'Could not delete order with id: {order_id}')
                self.set_status(500)
                self.write({"success": False, "message": "could not delete order"})


class OrderSingle(BaseHandler):
    @access_token_required
    @json_required
    def post(self):
        with Db() as session:
            try:
                if 'product_id' not in self.data or 'quantity' not in self.data or \
                    (type(self.data['product_id']) != int or type(self.data['quantity']) != int) :
                    self.set_status(400)
                    self.write({"message": "product_id and quantity are required to place an \
                                              order.product_id (int) and quantity (int) should contain a \
                                              single value enclosed."})
                    return

                product_id = int(self.data['product_id'])
                quantity = int(self.data['quantity'])

                logger.info(f"Product id: {product_id}, quantity: {quantity}")

                # get the product
                product = session.query(Product).filter(Product.id==product_id).first()

                if product.stock_quantity == 0:
                    self.set_status(404)
                    self.write({"message": "Item is out of stock."})
                    return
                if product.stock_quantity < quantity:
                    self.set_status(409)
                    self.write({"message": f"Not enough stock available. Only {product.stock_quantity} items left."})
                    return

                # place the order
                # total_amount = product.price * quantity
                logger.info(f"Current User is: {uuid.UUID(bytes=self.current_user.id)}")
                current_user = session.query(User).filter(User.id==self.current_user.id).first()
                order = session.query(Order).filter(Order.ordered_by==current_user.id,\
                                                    Order.status==OrderStatus.pending.value).first()
                if order:
                    found = False
                    for item in order.order_items:
                        if item.product_id == product_id:
                            logger.info("%s %s" %(item.product_id, product_id))
                            item.quantity += 1
                            item.product.stock_quantity -= 1
                            session.commit()
                            found = True
                    if not found:
                        order_item = OrderItem(quantity=quantity, unitprice=product.price, order_id=order.id, product_id=product.id)
                        product = session.query(Product).filter(Product.id==product_id).first()
                        product.stock_quantity -= quantity
                        session.add(order_item)
                        session.commit()

                else:
                    order = Order(ordered_by=current_user.id)
                    session.add(order)
                    session.commit()
                    logger.info(f"Order placed! {order.id} for {order.total}")
                    # place individual order items
                    order_item = OrderItem(quantity=quantity, unitprice=product.price, order_id=order.id, product_id=product.id)
                    product = session.query(Product).filter(Product.id==product_id).first()
                    product.stock_quantity -= quantity
                    session.add(order_item)
                    session.commit()

                self.write({'order_id': order.id})
            except Exception as e:
                logger.info(f"Could not order! {e}")
                self.set_status(500)
                self.write({"message": "Something went wrong!"})
                return

    @access_token_required
    def get(self, order_id):
        with Db() as session:
            try:
                logger.info("Order: %s"%order_id)
                order = session.query(Order).filter(Order.id==order_id, Order.ordered_by==self.current_user.id).first()
                if order:
                    self.write(json.dumps(Order.get_json_value(order)))
                else:
                    self.status(400)
                    self.write({"message": "order not found!"})
            except json.JSONDecodeError:
                self.set_status(400)
                self.write({"message": "Expected JSON in request body. Got None"})
                return


class OrderList(BaseHandler):
    @access_token_required
    def get(self):
        with Db() as session:
            try:
                orders = session.query(Order).filter(Order.ordered_by==self.current_user.id,\
                                                     or_((Order.status==OrderStatus.completed.value), \
                                                        (Order.status==OrderStatus.shipped.value),\
                                                        (Order.status==OrderStatus.delivered.value))).all()
                logger.info(orders)
                # logger.info("User %s" %self.current_user.id)
                if orders:
                    self.write({"orders": Order.get_json_values(orders)})
                else:
                    self.set_status(200)
                    self.write({"message": "No orders to show!"})
            except Exception as e:
                logger.exception(f"Could not process! {e}")
                self.set_status(500)
                self.write({"message": "Could not get orders!"})
