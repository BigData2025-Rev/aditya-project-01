from service.basehandler import BaseHandler
import uuid

from model.user import User
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
