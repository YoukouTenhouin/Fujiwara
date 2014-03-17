import tornado.web
import os
import pymongo
import redis

from Fujiwara.handlers.apis import handlers as apis
from Fujiwara.handlers.views import handlers as views
from Fujiwara.handlers.user import handlers as userpages
from Fujiwara.auth import Auth

class Application(tornado.web.Application):
    def __init__(self,key,*args,**kwargs):
        handlers = apis
        handlers.extend(views)
        handlers.extend(userpages)

        self.mongo = pymongo.Connection().fujiwara
        self.redis = redis.StrictRedis()

        self.auth = Auth(key)
        root = os.path.dirname(__file__)
        template_path = os.path.join(root,'../templates')
        tornado.web.Application.__init__(self,handlers,template_path=template_path,*args,**kwargs)
