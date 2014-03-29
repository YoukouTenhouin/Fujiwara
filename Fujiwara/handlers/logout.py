from Fujiwara.handlers import Base
from Fujiwara.decorators import login_requested

class Logout(Base):
    @login_requested
    def get(self):
        self.clear_cookie('userinfo')
        try:
            referer = self.request.headers['referer']
        except:
            referer = '/'

        self.redirect(referer)
