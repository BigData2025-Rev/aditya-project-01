import tornado.web
from sqlalchemy import or_
from db.session import session as Db
import json

from logger.logger import logger
from model.user import User


class Register(tornado.web.RequestHandler):
    def post(self):
        try:
            with Db() as session:
                try:
                    data = json.loads(self.request.body)
                except json.JSONDecodeError:
                    self.set_status(400)
                    self.write({"message": "Expected JSON in request body. Got None"})
                    return

                # logger.debug("Data :%s" %data)
                if not ('password' in data and 'username' in data and 'email' in data and 'country' in data):
                    self.set_status(400)
                    self.write({"message": "username, password, email or country cannot be empty!"})
                    return
                # logger.debug("Request body -> email: %s" %data['username'])

                user_exists = False
                
                try:
                    user_exists = session.query(User).filter(or_(User.username==data['username'], User.email==data['email'])).first()
                    logger.info("User exists: %s"%user_exists)
                except Exception as e:
                    self.set_status(409)
                    self.write("A user with the email exists. Try signing in.\n")


                if user_exists:
                    self.set_status(409)
                    self.write("A user with the email exists. Try signing in.\n")


                if not user_exists:
                    new_user = User(username=data['username'], email=data['email'], country=data['country'])
                    new_user.set_password(data['password'])
                    session.add(new_user)
                    session.commit()
                
                    self.write({"message": f"Hi {new_user.username}, you are registered!", "status": "success"})
                

        except Exception as e:
            logger.exception(str(e))
