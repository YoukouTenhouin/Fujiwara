import tornado.web
import os
import pymongo
import redis

from Fujiwara.handlers import handlers
from Fujiwara.auth import Auth

class Application(tornado.web.Application):
    def __init__(self,key,*args,**kwargs):
        self.mongo = pymongo.Connection().fujiwara
        self.redis = redis.StrictRedis()

        self.auth = Auth(key)
        root = os.path.dirname(__file__)
        template_path = os.path.join(root,'../templates')
        tornado.web.Application.__init__(self,handlers,template_path=template_path,*args,**kwargs)
