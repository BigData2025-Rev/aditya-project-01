import tornado.web
import json
import uuid

from db.session import session as Db
from logger.logger import logger
from model.user import User
from model.order import Order
from utils.decorators.adminaccess import admin_required
from utils.decorators.useraccess import access_token_required

class AdminGetUsers(tornado.web.RequestHandler):

    @access_token_required
    @admin_required
    def get(self):
        try:
            limit = 100
            offset = 0
            logger.info("Here")
            if self.request.body:
                data = json.loads(self.request.body)
                logger.info("json data: %s" %data)
                
                if data:
                    if 'limit' in data:
                        limit = data['limit']
                    if 'offset' in data:
                        offset = data['offset']

            with Db() as session:
                users = session.query(User).offset(offset).limit(limit).all()
                prepared_response = []
                for user in users:
                    temp = {}
                    temp['id'] = str(uuid.UUID(bytes=user.id))
                    temp['username'] = user.username
                    temp['created_at'] = str(user.created_at)
                    prepared_response.append(temp)
                logger.info("Users: %s"%users)
                self.write({"users": prepared_response})
        except Exception as e:
            self.set_status(500)
            logger.exception(f"API Exception: {e}")
            self.write({"message": "Could not get users!"})


class AdminGetOrders(tornado.web.RequestHandler):
    @access_token_required
    @admin_required
    def get(self):
        try:
            data = json.loads(self.request.body)
            if data:
                if 'limit' in data:
                    limit = data['limit']
                if 'offset' in data:
                    offset = data['offset']
        except json.JSONDecodeError:
            pass

        try:
            limit = 100
            offset = 0
            with Db() as session:
                orders = session.query(Order).offset(offset).limit(limit).all()
                logger.info("Orders: %s" %orders)
                self.write({"orders": Order.get_json_values(orders)})
        except Exception:
            self.set_status(500)
            self.write({"message": "Could not get orders!"})
