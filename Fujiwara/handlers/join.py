from Fujiwara.handlers import Base
from Fujiwara.decorators import check_recaptcha

from hashlib import sha256
from datetime import datetime

class Join(Base):
    def get(self):
        fields = {
            'name':'',
            'email':''
        }

        errors = {
            'user_exists':False,
            'captcha_unmatch':False
        }

        self.render('join.html',
                    fields = fields,
                    errors = errors,
                    pubkey = self.settings['recaptcha_pubkey'])

    @check_recaptcha
    def post(self,captcha):
        errors = {
            'user_exists':False,
            'captcha_unmatch':False
        }

        error = False

        name = self.get_argument('name')
        pwd = self.get_argument('pwd')
        email = self.get_argument('email')

        fields = {
            'name':name,
            'email':email
        }

        if not captcha:
            errors['captcha_unmatch'] = True
            self.render('join.html',
                        errors = errors,
                        fields = fields,
                        pubkey = self.settings['recaptcha_pubkey'])
            return

        name = name.strip()
        name_lower = name.lower()
        ret = self.mongo.users.find({'name_lower':name_lower})
        if ret.count() > 0:
            error = True
            errors['user_exists'] = True

        if error:
            self.render('join.html',
                        errors = errors,
                        fields = fields,
                        pubkey = self.settings['recaptcha_pubkey'])
            return
            
        # No error,continue
        hashed_pwd = sha256(pwd.encode()).hexdigest()
        user = {
            'name':name,
            'name_lower':name_lower,
            'hashed_pwd':hashed_pwd,
            'email':email.strip(),
            'jobs':[]
        }

        uid = self.mongo.users.insert(user)
        cookie = self.auth.encodeData({"uid":uid})

        self.set_cookie('userinfo',cookie,
                        expires=datetime(3000,1,1))

        self.redirect('/')
