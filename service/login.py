from service.basehandler import BaseHandler
import json
import jwt
import os
import datetime

from db.session import session as Db
from logger.logger import logger

from model.user import User
from utils.decorators.request import json_required

class Login(BaseHandler):
    @json_required
    def post(self):
        with Db() as session:
            # logger.info("Data: %s" %data)
            if not ('username' in self.data and 'password' in self.data):
                self.send_error(400)
                return

            try:
                user = session.query(User).filter(User.username==self.data['username']).first()
                logger.debug("User Exists: %s" %user)
                if not user:
                    logger.info("User not found! %s" %self.data['username'])
                    self.set_status(401)
                    self.write({"User not found! Try registering first.\n"})
                    return

                logger.info("User: %s" %user)
                logger.info("Password correct for user %s -> %s"%(user.username, user.check_password(self.data['password'])))
                if user.check_password(self.data['password']):
                    expiration = datetime.datetime.now() + datetime.timedelta(minutes=50)
                    token = jwt.encode({"sub": user.username, "exp": expiration.timestamp()},
                                        os.getenv('JWT_SECRET'), algorithm="HS256")
                    logger.debug("token %s" %token)
                    self.write({"token": token, "role": user.role, "success": True})
                else:
                    self.set_status(401)
                    self.write({"message": "Incorrect password!"})

            except Exception as e:
                logger.info(e)

            except Exception as e:
                pass
