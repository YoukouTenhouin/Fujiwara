from Fujiwara.handlers.apis import ApiBase
from Fujiwara.decorators import logind

from hashlib import sha256

import datetime

class Logout(ApiBase):
    def post(self):
        self.clear_cookie('userinfo')
        self.write({'success':True})
        
class Login(ApiBase):
    def post(self):
        username = self.get_argument('user')
        pwd = self.get_argument('pwd')

        username = username.lower()
        pwd = pwd.encode()
        
        hashed_pwd = sha256(pwd).hexdigest()

        users = self.mongo.users.find({"name_lower":username,
                                       "hashed_pwd":hashed_pwd})
        
        if users.count() != 0:
            uid = users[0]['_id']
            cookie = self.auth.encodeData({"uid":uid})
            self.set_cookie('userinfo',cookie,expires=datetime.datetime(3000,1,1))
            ret = {'success':True}
        else:
            ret = {'success':False}

        self.write(ret)

class Info(ApiBase):
    @logind({'logind':False})
    def get(self,user):
        user['_id'] = str(user['_id'])
        del user['name_lower']
        del user['hashed_pwd']

        user['logind'] = True        
        self.write(user)
