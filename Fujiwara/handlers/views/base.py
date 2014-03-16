from Fujiwara.handlers.base import Base

class ViewBase(Base):
    def render(self,*args,**kwargs):
        Base.render(self,mongo = self.mongo,*args,**kwargs)
