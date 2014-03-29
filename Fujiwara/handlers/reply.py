from Fujiwara.handlers import Base
from Fujiwara.decorators import login_requested

from datetime import datetime
from bson.objectid import ObjectId

class Reply(Base):
    def post(self,tid):
        tid = ObjectId(tid)

        if self.mongo.threads.find({'_id':tid}).count() == 0:
            raise HTTPError(404)

        now = datetime.now()

        content = self.get_argument('content')
        replyto = self.get_argument('replyto')
        replyto = set(replyto.split(','))
        replyto = [ObjectId(i) for i in replyto]
        
        pid = self.mongo.posts.insert({'content':content,
                                       'datetime':now,
                                       'th':ObjectId(tid),
                                       'author':self.user['_id'],
                                       'replyto':replyto})

        self.mongo.threads.update(
            {'_id':ObjectId(tid)},
            {'$set':{'lastreply':now}}
        )

        try:
            referer = self.request.headers['referer']
        except:
            referer = '/thread/view'%tid

        self.redirect(referer)
