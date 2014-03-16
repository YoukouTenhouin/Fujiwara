from Fujiwara.handlers import Base

class ApiBase(Base):
    @property
    def auth(self):
        return self.application.auth
