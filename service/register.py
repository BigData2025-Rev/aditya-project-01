from service.basehandler import BaseHandler
from sqlalchemy import or_
from db.session import session as Db
import json

from logger.logger import logger
from model.user import User


class Register(BaseHandler):
    def post(self):
        try:
            with Db() as session:
                # logger.debug("Data :%s" %data)
                if not ('password' in self.data and 'username' in self.data and 'email' in self.data and 'country' in self.data):
                    self.set_status(400)
                    self.write({"message": "username, password, email or country cannot be empty!"})
                    return
                # logger.debug("Request body -> email: %s" %self.self.data['username'])

                user_exists = False

                try:
                    user_exists = session.query(User).filter(or_(User.username==self.data['username'], User.email==self.data['email'])).first()
                    logger.info("User exists: %s"%user_exists)
                except Exception as e:
                    self.set_status(409)
                    self.write("A user with the email exists. Try signing in.\n")


                if user_exists:
                    self.set_status(409)
                    self.write("A user with the email exists. Try signing in.\n")


                if not user_exists:
                    new_user = User(username=self.data['username'], email=self.data['email'], country=self.data['country'])
                    if 'deposit_amount' in self.data:
                        new_user = User(username=self.data['username'],\
                                    email=self.data['email'], country=self.data['country'],
                                    wallet_balance=self.data['deposit_amount'])

                    new_user.set_password(self.data['password'])
                    session.add(new_user)
                    session.commit()

                    self.write({"message": f"Hi {new_user.username}, you are registered!", "status": "success"})


        except Exception as e:
            logger.exception(str(e))
