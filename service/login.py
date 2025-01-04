import tornado.web
import json
import jwt
import os
import datetime

from db.session import session as Db
from logger.logger import logger

from model.user import User

class Login(tornado.web.RequestHandler):
    def post(self):
        with Db() as session:
            try:
                data = json.loads(self.request.body)
            except json.JSONDecodeError:
                self.set_status(400)
                self.write({"message": "Expected JSON in request body. Got None"})
                return

            # logger.info("Data: %s" %data)
            if not ('username' in data and 'password' in data):
                self.send_error(400)
                return

            try:
                user = session.query(User).filter(User.username==data['username']).first()
                logger.debug("User Exists: %s" %user)
                if not user:
                    logger.info("User not found! %s" %data['username'])
                    self.write("User not found! Try registering first.\n")
                    return

                logger.info("User: %s" %user)
                logger.info("Password correct for user %s -> %s"%(user.username, user.check_password(data['password'])))
                if user.check_password(data['password']):
                    expiration = datetime.datetime.now() + datetime.timedelta(minutes=50)
                    token = jwt.encode({"sub": user.username, "exp": expiration.timestamp()},
                                        os.getenv('JWT_SECRET'), algorithm="HS256")
                    logger.debug("token %s" %token)
                    self.write({"token": token})

            except Exception as e:
                logger.info(e)

            except Exception as e:
                pass
