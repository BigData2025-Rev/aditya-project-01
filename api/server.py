import tornado.ioloop
import tornado.web
import asyncio
import sys
import os
import signal
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logger.logger import logger
from service.register import Register
from service.login import Login
from service.admin import AdminGetUsers, AdminGetOrders
from service.product import ProductList
from service.order import OrderSingle, OrderList
from db.base import Base, engine


routes = [
    (r'/register', Register),
    (r'/login', Login),
    (r'/getallusers',AdminGetUsers),
    (r'/products', ProductList),
    (r'/order', OrderSingle),
    (r'/order/(\d+)', OrderSingle),
    (r'/orders', OrderList),
    (r'/getallorders', AdminGetOrders)

]


def start():
    Base.metadata.create_all(engine)

start()

async def main():
    
    application = tornado.web.Application(routes)
    application.listen(8888)
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down...")
