import tornado.web

class Base(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Server","Tsuchimikado")
        
    @property
    def mongo(self):
        return self.application.mongo

    @property
    def redis(self):
        return self.application.redis

    @property
    def auth(self):
        return self.application.auth
