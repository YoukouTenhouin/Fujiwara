from Fujiwara.handlers.apis import ApiBase
from hashlib import sha256

class Register(ApiBase):
    def post(self):
        username = self.get_argument('user')
        pwd = self.get_argument('pwd')
        email = self.get_argument('email')

        if len(username) == 0 or len(pwd) == 0:
            self.write({
                'success':False,
                'code':2,
                'reason':'form not filled'})
            return

        # Check wheater user exists
        if self.mongo.users.find({'name_lower':username.strip().lower()}).count() != 0:
            self.write({
                'success':False,
                'code':1,
                'reason':'user exists'})
            return

        hashed_pwd = sha256(pwd.encode()).hexdigest()
        
        uid = self.mongo.users.insert({
            'name':username,
            'name_lower':username.strip().lower(),
            'hashed_pwd':hashed_pwd,
            'email':email
        })

        # Login
        cookie = self.auth.encodeData({"uid":uid})
        self.set_cookie('userinfo',cookie)
        
        self.write({'success':True})
