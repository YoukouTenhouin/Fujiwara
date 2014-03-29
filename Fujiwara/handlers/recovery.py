from Fujiwara.handlers import Base
from Fujiwara.decorators import admin_requested

from bson.objectid import ObjectId

class RecoverThread(Base):
    @admin_requested
    def get(self,tid):
        tid = ObjectId(tid)
        self.mongo.threads.update(
            {'_id':tid},
            {'$set':{'hidden':False}}
        )

        referer = self.request.headers['referer']
        self.redirect(referer)

class RecoverPost(Base):
    @admin_requested
    def get(self,pid):
        pid = ObjectId(pid)
        self.mongo.posts.update(
            {'_id':pid},
            {'$set':{'hidden':False}}
        )

        referer = self.request.headers['referer']
        self.redirect(referer)
