import tornado.ioloop
import tornado.web
import tornado.escape


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        # Set the CORS headers for every response
        self.set_header("Access-Control-Allow-Origin", "*")  # Allow all origins
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PATCH, DELETE")  # Allow methods
        self.set_header("Access-Control-Allow-Headers", "Content-Type")  # Allow Content-Type header

    def options(self):
        # Handle OPTIONS requests (preflight)
        self.set_status(204)  # No content
        self.finish()  # End the request
