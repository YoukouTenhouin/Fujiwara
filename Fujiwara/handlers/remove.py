from Fujiwara.handlers import Base
from Fujiwara.decorators import admin_requested

from bson.objectid import ObjectId

class RemoveThread(Base):
    @admin_requested
    def get(self,tid):
        self.mongo.threads.update(
            {'_id':ObjectId(tid)},
            {'$set':{'hidden':True}}
        )

        self.redirect('/')

class RemovePost(Base):
    @admin_requested
    def get(self,pid):
        self.mongo.posts.update(
            {'_id':ObjectId(pid)},
            {'$set':{'hidden':True}}
        )

        referer = self.request.headers['referer']
        self.redirect(referer)
