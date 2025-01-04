import tornado.web
import json
import os
import datetime

from db.session import session as Db
from logger.logger import logger

from model.user import User

class UserUpdateData(tornado.web.RequestHandler):
    pass