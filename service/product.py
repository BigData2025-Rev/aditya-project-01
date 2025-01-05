import tornado.web
import json
import os
import datetime
import random

from db.session import session as Db
from logger.logger import logger

from model.product import Product
from model.category import Category
from utils.decorators.useraccess import access_token_required

class ProductList(tornado.web.RequestHandler):

    @access_token_required
    def get(self):
        try:
            limit = 20
            with Db() as session:
                product_count = session.query(Product).count()
                random_offset = random.randint(0, product_count-limit)
                products = session.query(Product).offset(random_offset).limit(limit).all()
                prepared_response = []
                for product in products:
                    category = session.query(Category).filter_by(id=product.category_id).first()
                    temp = {}
                    temp['product_id'] = product.id
                    temp['name'] = product.name
                    temp['rating'] = product.rating
                    temp['stock'] = product.stock_quantity
                    temp['number of ratings'] = product.no_of_ratings
                    temp['category'] = category.name
                    temp['price'] = f"{product.price:.2f}"
                    prepared_response.append(temp)

                self.write({"products": prepared_response})

        except:
            self.set_status(500)
            self.write({"message": "Something went wrong!"})
