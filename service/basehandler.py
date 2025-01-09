import tornado.ioloop
import tornado.web
import tornado.escape


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PATCH, DELETE")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def options(self, *args, **kwargs):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PATCH, DELETE")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, X-Custom-Header, Authorization")
        self.set_status(204)
        self.finish()
