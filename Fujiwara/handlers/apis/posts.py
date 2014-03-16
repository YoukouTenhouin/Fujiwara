from Fujiwara.handlers.apis import ApiBase
from bson.objectid import ObjectId

import datetime

class PostAdd(ApiBase):
    def post(self):
        now = datetime.datetime.now()

        cookie = self.get_cookie('userinfo')
        if not self.auth.vaild(cookie):
            self.write({'success':False,'error':1})
            return

        uid = self.auth.decodeData(cookie)['uid']
            
        content = self.get_argument('content')
        tid = self.get_argument('tid')
        replyto = self.get_argument('replyto')
        replyto = set(replyto.split(','))
        replyto = [ObjectId(i) for i in replyto]
        
        pid = self.mongo.posts.insert({'content':content,
                                       'datetime':now,
                                       'th':ObjectId(tid),
                                       'author':uid,
                                       'replyto':replyto})

        self.mongo.threads.update(
            {'_id':ObjectId(tid)},
            {'$set':{'lastreply':now}}
        )
        
        self.write({'success':True})

class PostDel(ApiBase):
    def post(self):
        cookie = self.get_cookie('userinfo')
        if not self.auth.vaild(cookie):
            self.write({'success':False,'error':1})
            return

        uid = self.auth.decodeData(cookie)['uid']
        user = self.mongo.users.find({'_id':uid})[0]
            
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
    def post(self):
        cookie = self.get_cookie('userinfo')
        if not self.auth.vaild(cookie):
            self.write({'success':False,'error':1})
            return

        uid = self.auth.decodeData(cookie)['uid']
        user = self.mongo.users.find({'_id':uid})[0]
        
        pid = self.get_argument('pid')
        content = self.get_argument('content')
        
        self.mongo.posts.update(
            {'_id':ObjectId(pid),'author':user['_id']},
            {'$set':{'content':content}}
        )
        
        self.write({'success':True})
