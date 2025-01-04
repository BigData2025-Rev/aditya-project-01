from functools import wraps
import jwt
import os
import time
from db.session import session as Db
from model.user import User, Role
from logger.logger import logger

SECRET_KEY=os.getenv('JWT_SECRET')


def access_token_required(f):
    def check_token(self, *args, **kwargs):
        token = self.request.headers.get("Authorization")
        
        if not token:
            self.set_status(401)
            self.write({'message': 'Token is missing!'})
            return

        try:
            token = token.split(" ")[1]
            # logger.info("User token: %s" %token)
            with Db() as session:
                data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                self.current_user = session.query(User).filter_by(username=data['sub']).first()
                logger.info("CurrentRole: %s" %(self.current_user.role_enum))
        except jwt.DecodeError:
            self.set_status(403)
            self.write({'message': 'Token is invalid!'})
            return
        except:
            self.set_status(403)
            self.write({'message': 'Token is invalid!'})
            return
        return f(self, *args, **kwargs)
    return check_token
