from Fujiwara.handlers import Base

from datetime import datetime
from hashlib import sha256

class Login(Base):
    def get(self):
        fields = {'name':''}
        errors = {'incorrect':False}

        try:
            referer = self.request.headers['referer']
        except:
            referer = '/'
        
        self.render('login.html',
                    fields=fields,
                    errors=errors,
                    referer = referer)

    def post(self):
        fields = { 'name':'' }
        errors = { 'incorrect':False }

        error = False

        name = self.get_argument('name').strip()
        name_lower = name.lower()
        pwd = self.get_argument('pwd')
        referer = self.get_argument('referer')
        hashed_pwd = sha256(pwd.encode()).hexdigest()

        fields['name'] = name

        res = self.mongo.users.find({'name_lower':name_lower,
                                     'hashed_pwd':hashed_pwd})

        if res.count() == 0:
            errors['incorrent'] = True
            error = True

        if error:
            self.render('login.html',
                        errors = errors,
                        fields = fields)
            return

        user = res[0]

        uid = user['_id']
        cookie = self.auth.encodeData({'uid':uid})

        self.set_cookie('userinfo',cookie,
                        expires=datetime(3000,1,1))

        self.redirect(referer)
