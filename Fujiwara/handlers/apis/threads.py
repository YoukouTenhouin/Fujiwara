from Fujiwara.handlers.apis.base import ApiBase
from Fujiwara.decorators import logind
from bson.objectid import ObjectId

import datetime

class ThreadAdd(ApiBase):
    @logind()
    def post(self,user):
        now = datetime.datetime.now()

        # Get arguments
        title = self.get_argument('title')
        content = self.get_argument('content')
        tags = self.get_argument('tags').split(',')
        tags = [i.strip() for i in tags]
        
        if len(title) == 0:
            self.write({'success':False,'error':2})
            return
            
        tid = self.mongo.threads.insert({'title':title,
                                         'author':uid,
                                         'datetime':now,
                                         'lastreply':now,
                                         'tags':tags})
        
        self.mongo.posts.insert({'author':user['_id'],
                                 'datetime':now,
                                 'th':tid,
                                 'content':content})
                       
        self.write({'success':True,'tid':str(tid)})

class ThreadDel(ApiBase):
    @logind()
    def post(self,user):
        if not 'admin' in user['jobs']:
            self.write({'success':False,'error':2})
            return
                
        tid = self.get_argument('tid')

        self.mongo.threads.update(
            {'_id':ObjectId(tid)},
            {'$set':{'hidden':True}}
        )
        
        self.write({'success':True})

class ThreadUpdate(ApiBase):
    @logind()
    def post(self,user):
        tid = self.get_argument('tid')
        res = self.mongo.threads.find({'_id':ObjectId(tid)})
        if res.count() == 0:
            raise tornado.web.HTTPError(404)

        thread = res[0]

        tags = self.get_argument('tags').split(',')
        tags = [i.strip() for i in tags]
        title = self.get_argument('title')
            
        self.mongo.threads.update(
            {'_id':ObjectId(tid),'author':user['_id']},
            {'$set':{'title':title,'tags':tags}}
        );
        
        self.write({'success':True})







