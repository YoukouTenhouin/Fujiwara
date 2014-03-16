from Fujiwara.handlers.apis import ApiBase

class UserInfo(ApiBase):
    def get(self):
        cookie = self.get_cookie('userinfo')
        
        if not self.auth.vaild(cookie):
            self.clear_cookie('userinfo')
            self.write({'logind':False})
            return

        uid = self.auth.decodeData(cookie)['uid']
            
        #Get user from database
        user = self.mongo.users.find({'_id':uid})[0]
        
        user['_id'] = str(user['_id'])
        del user['name_lower']
        del user['hashed_pwd']

        user['logind'] = True        
        self.write(user)
