import tornado.web
import json
import uuid
from sqlalchemy.exc import IntegrityError, OperationalError, DataError, DatabaseError, StatementError

from db.session import session as Db
from logger.logger import logger
from model.user import User, Role
from model.order import Order, OrderStatus
from utils.decorators.adminaccess import admin_required
from utils.decorators.useraccess import access_token_required
from utils.decorators.request import json_required, json_optional


class AdminGetUsers(tornado.web.RequestHandler):

    @access_token_required
    @admin_required
    @json_optional
    def get(self):
        limit = 100
        offset = 0
        if self.data:
            if 'limit' in self.data:
                limit = self.data['limit']
            if 'offset' in self.data:
                offset = self.data['offset']

        try:
            with Db() as session:
                users = session.query(User).offset(offset).limit(limit).all()
                prepared_response = []
                for user in users:
                    temp = {}
                    temp['id'] = str(uuid.UUID(bytes=user.id))
                    temp['username'] = user.username
                    temp['created_at'] = str(user.created_at)
                    temp['role'] = str(user.role)
                    prepared_response.append(temp)
                logger.info("Users: %s"%users)
                self.write({"users": prepared_response})
        except Exception as e:
            self.set_status(500)
            logger.info(f"API Exception: {e}")
            self.write({"message": "Could not get users!"})


class AdminGetOrders(tornado.web.RequestHandler):
    @access_token_required
    @admin_required
    @json_optional
    def get(self):
        limit = 100
        offset = 0
        if self.data:
            if 'limit' in self.data:
                limit = self.data['limit']
            if 'offset' in self.data:
                offset = self.data['offset']

        try:
            limit = 100
            offset = 0
            with Db() as session:
                orders = session.query(Order).offset(offset).limit(limit).all()
                # logger.info("Orders: %s" %orders)
                self.write({"orders": Order.get_json_values(orders)})
        except Exception:
            self.set_status(500)
            self.write({"message": "Could not get orders!"})


class AdminRemoveUser(tornado.web.RequestHandler):
    @access_token_required
    @admin_required
    def delete(self, user_id):
        with Db() as session:
            try:
                session.query(User).filter(User.id==uuid.UUID(user_id).bytes).delete(synchronize_session='evaluate')
                session.commit()
                self.write({"message": "Success!"})
            except Exception as e:
                logger.info(f"Could not delete user: {e}")
                session.rollback()
                self.set_status(500)


class AdminUpdateUser(tornado.web.RequestHandler):
    @access_token_required
    @admin_required
    @json_required
    def patch(self, user_id):
        with Db() as session:
            try:
                if 'username' in self.data or 'role' in self.data or 'email' in self.data or 'password' in self.data:
                    if 'username' in self.data:
                        session.query(User).filter(User.id==uuid.UUID(user_id).bytes).update({"username": self.data['username']})
                        session.commit()

                    if 'role' in self.data:
                        session.query(User).filter(User.id==uuid.UUID(user_id).bytes).update({"role": Role[self.data['role']].value})
                        session.commit()

                    if 'email' in self.data:
                        session.query(User).filter(User.id==uuid.UUID(user_id).bytes).update({"email": self.data['email']})
                        session.commit()

                    if 'password' in self.data:
                        user = session.query(User).filter(User.id==uuid.UUID(user_id).bytes).first()
                        if user:
                            user.set_password(self.data['password'])
                            session.commit()

                    self.write({"message": "Success!"})

            except (IntegrityError, OperationalError, DataError, DatabaseError, StatementError) as e:
                logger.info(f"Could not update! {e}")
                session.rollback()
            except Exception as e:
                logger.info(f"Could not update user: {e}")
                self.set_status(400)
                self.write({"message": "Expected JSON in request body. Got None"})


class AdminUpdateOrder(tornado.web.RequestHandler):
    @access_token_required
    @admin_required
    @json_required
    def patch(self, order_id):
        with Db() as session:
            try:
                if 'order_status' in self.data:
                    order = session.query(Order).filter(Order.id==order_id).first()
                    if order:
                        order.status = OrderStatus[self.data['order_status']].value
                        session.commit()
                        self.write({"message": "Success!"})

            except (IntegrityError, OperationalError, DataError, DatabaseError, StatementError) as e:
                logger.info(f"Could not update! {e}")
                session.rollback()
            except Exception as e:
                logger.info(f"Could not update order: {e}")
                self.set_status(400)
                self.write({"message": "Could not update order, check request body."})
