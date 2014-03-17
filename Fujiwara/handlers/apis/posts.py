from Fujiwara.handlers.apis import ApiBase
from Fujiwara.decorators import logind
from bson.objectid import ObjectId

import datetime

class PostAdd(ApiBase):
    @logind()
    def post(self,user):
        now = datetime.datetime.now()

        content = self.get_argument('content')
        tid = self.get_argument('tid')
        replyto = self.get_argument('replyto')
        replyto = set(replyto.split(','))
        replyto = [ObjectId(i) for i in replyto]
        
        pid = self.mongo.posts.insert({'content':content,
                                       'datetime':now,
                                       'th':ObjectId(tid),
                                       'author':user['_id'],
                                       'replyto':replyto})

        self.mongo.threads.update(
            {'_id':ObjectId(tid)},
            {'$set':{'lastreply':now}}
        )
        
        self.write({'success':True})

class PostDel(ApiBase):
    @logind()
    def post(self,user):
        if not 'admin' in user['jobs']:
            self.write({'success':False,'error':2})
            return

        pid = self.get_argument('pid')
        
        self.mongo.posts.update(
            {'_id':ObjectId(pid)},
            {'$set':{'hidden':True}}
        )

        self.write({'success':True})

class PostUpdate(ApiBase):
    @logind()
    def post(self,user):
        pid = self.get_argument('pid')
        content = self.get_argument('content')
        
        self.mongo.posts.update(
            {'_id':ObjectId(pid),'author':user['_id']},
            {'$set':{'content':content}}
        )
        
        self.write({'success':True})
