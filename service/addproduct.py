from service.basehandler import BaseHandler
import json

from db.session import session as Db
from pydantic import BaseModel
from typing import List

from logger.logger import logger
from model.product import Product

class Product(BaseModel):
    name: str
    price: float
    category: str


class AddProduct(BaseHandler):
    def post(self):
        raw = json.loads(self.request.body)
        logger.info(raw)
        if not isinstance(raw, list):
            raise ValueError("Input should be a list of dictionaries.")
        
        data = [Product.parse_obj(item) for item in raw]
        for d in data:
            logger.info("%s %s %s " %(d.name, d.price, d.category))
