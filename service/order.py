import tornado.web
import json
import os
import datetime
import random
import uuid

from db.session import session as Db
from logger.logger import logger

from model.order import Order, OrderStatus
from model.orderitem import OrderItem
from model.product import Product
from model.user import User
from utils.decorators.useraccess import access_token_required

class OrderSingle(tornado.web.RequestHandler):

    @access_token_required
    def post(self):
        with Db() as session:
            try:
                data = json.loads(self.request.body)
            except json.JSONDecodeError:
                self.set_status(400)
                self.write({"message": "Expected JSON in request body. Got None"})
                return
            
            try:
                
                if 'product_id' not in data or 'quantity' not in data or \
                    (type(data['product_id']) != int or type(data['quantity']) != int) :
                    self.set_status(400)
                    self.write({"""message": "product_id and quantity are required to place an order.product_id (int) and quantity (int) should contain a single value enclosed."""})
                    return
                
                product_id = int(data['product_id'])
                quantity = int(data['quantity'])

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
                total_amount = product.price * quantity
                # logger.info("HERE>>>>>>>>>>>>>")
                order = Order(ordered_by=self.current_user.id, total=total_amount)
                session.add(order)
                session.commit()
                
                persisted_order = session.query(Order).filter(Order.ordered_by==self.current_user.id).first()
                

                # place individual order items
                order_item = OrderItem(quantity=quantity, unitprice=product.price, order_id=persisted_order.id, product_id=product.id)
                session.add(order_item)
                session.commit()

                product.stock_quantity -= quantity
                session.commit()
                self.write({'order_id': order.id, "total_amount": f"{total_amount:.2f}"})
            except Exception as e:
                logger.info(f"Could not order! {e}")
                self.set_status(500)
                self.write({"message": "Something went wrong!"})
                return
    
    @access_token_required
    def get(self, order_id):
        with Db() as session:
            try:
                logger.info("Order>>>>>>>>: %s"%order_id)
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

class OrderList(tornado.web.RequestHandler):
    @access_token_required
    def get(self):
        with Db() as session:
            try:
                orders = session.query(Order).filter(Order.ordered_by==self.current_user.id).all()
                logger.info("User %s" %self.current_user.id)
                if orders:
                    self.write({"orders": Order.get_json_values(orders)})
                else:
                    self.status(200)
                    self.write({"message": "No orders to show!"})
            except Exception as e:
                logger.exception(f"Could not process! {e}")
                self.set_status(500)
                self.write({"message": "Could not get orders!"})
