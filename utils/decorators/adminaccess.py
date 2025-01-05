from functools import wraps
import os
from db.session import session as Db
from model.user import Role
from logger.logger import logger


def admin_required(f):
    """
    NOTE: This decorator needs to be wrapped by a user level decorator,
          auth_token_required.
    """
    def check_admin_role(self, *args, **kwargs):
        try:
            logger.info("Roles: %s %s"%(self.current_user.role_enum, Role.admin))
            if not self.current_user.role_enum == Role.admin:
                self.set_status(403)
                self.write({"message": "Admin access only!"})
                return
        except:
            logger.info("Admin check failed!")
        return f(self, *args, **kwargs)
    return check_admin_role
