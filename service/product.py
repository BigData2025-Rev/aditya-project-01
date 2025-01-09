from service.basehandler import BaseHandler
import json
import random

from db.session import session as Db
from logger.logger import logger

from model.product import Product
from model.category import Category
from utils.decorators.useraccess import access_token_required

class ProductList(BaseHandler):

    @access_token_required
    def get(self):
        try:
            limit = 15
            with Db() as session:
                products = session.query(Product).offset(11).limit(limit).all()
                prepared_response = []
                for product in products:
                    temp = {}
                    temp['product_id'] = product.id
                    temp['name'] = product.name
                    temp['image'] = product.image
                    temp['rating'] = product.rating
                    temp['stock'] = product.stock_quantity
                    temp['number of ratings'] = product.no_of_ratings
                    temp['category'] = product.categ.name
                    temp['price'] = f"{product.price:.2f}"
                    prepared_response.append(temp)

                self.set_status(200)
                self.write({"products": json.dumps(prepared_response)})

        except:
            self.set_status(500)
            self.write({"message": "Something went wrong!"})
