from tornado.web import RequestHandler

class Base(RequestHandler):
    @property
    def user(self):
        try:
            return self._user
        except:
            cookie = self.get_cookie('userinfo',None)
            if not self.auth.vaild(cookie):
                self.clear_cookie('userinfo')
                self._user = None
            else:
                uid = self.auth.decodeData(cookie)['uid']
                user = self.mongo.users.find({'_id':uid})[0]
                self._user = user
                return user

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
        
    def render(self,*args,**kwargs):
        RequestHandler.render(self,mongo = self.mongo,user = self.user,
                    *args,**kwargs)
