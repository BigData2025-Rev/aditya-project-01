from service.basehandler import BaseHandler
import uuid

from model.user import User
from model.order import Order
from model.order import OrderStatus
from db.session import session as Db
from logger.logger import logger

from utils.decorators.useraccess import access_token_required
from utils.decorators.request import json_required


class UserAddBalance(BaseHandler):
    @access_token_required
    @json_required
    def post(self):
        try:
            with Db() as session:
                user = session.query(User).filter(User.id==self.current_user.id).first()
                user.wallet_balance += self.data['deposit_amount']
                session.commit()
                self.write({"message": 
                            f"""Successfully deposited """ +
                            f"""amount {self.data['deposit_amount']},new balance is {user.wallet_balance}"""})
        except Exception as e:
            logger.info(f"Could not deposit amount {self.data['deposit_amount']} \
                        for user {str(uuid.UUID(bytes=user.id))}")


class UserCartCheckout(BaseHandler):
    @access_token_required
    def post(self):
        with Db() as session:
            try:
                orders = session.query(Order).filter(Order.ordered_by==self.current_user.id, \
                                                     Order.status==OrderStatus.pending.value).all()
                total = 0.0
                for order in orders:
                    order_items = order.order_items
                    for order_item in order_items:
                        product = order_item.product
                        if product.stock_quantity == 0:
                            self.set_status(404)
                            self.write({"message": "Product {product.name} is out of stock."})
                            return
                        if product.stock_quantity < order_item.quantity:
                            self.set_status(409)
                            self.write({"message": f"Not enough stock available for product {product.name}.\
                                        Only {product.stock_quantity} items left."})
                            return
                        total += order_item.subtotal


                user = session.query(User).filter(User.id==self.current_user.id).first()

                # logger.info("Current User balance: %s Total Amount: %s" %(user.wallet_balance, order.))
                if user.wallet_balance < total:
                    self.set_status(402)
                    self.write({"message": "You don't have enough balance. Please add funds to your account!"})
                    return

                user.wallet_balance-=total
                session.commit()

                for order in orders:
                    order.status = OrderStatus.completed.value
                session.commit()

                self.write({'order_id': order.id, "total_amount": f"{total:.2f}"})
            except Exception as e:
                logger.info(f"Could not order! {e}")
                self.set_status(500)
                self.write({"message": "Something went wrong!"})
                return


class UserCartList(BaseHandler):
    @access_token_required
    def get(self):
        with Db() as session:
            try:
                orders = session.query(Order).filter(Order.ordered_by==self.current_user.id, \
                                                     Order.status==OrderStatus.pending.value).all()
                self.write({"orders": Order.get_json_values(orders)})
            except Exception as e:
                logger.exception(f"Could not process! {e}")
                self.set_status(500)
                self.write({"message": "Could not get orders!"})
