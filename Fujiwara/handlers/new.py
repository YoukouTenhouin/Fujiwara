from Fujiwara.handlers import Base
from Fujiwara.decorators import login_requested

from tornado.web import HTTPError

from bson.objectid import ObjectId
from datetime import datetime

class New(Base):
    @login_requested
    def get(self):
        self.render('new.html')
        
    @login_requested
    def post(self):
        now = datetime.now()

        # Get arguments
        title = self.get_argument('title')
        content = self.get_argument('content')
        category = self.get_argument('category')
        
        try:
            cid = ObjectId(category)
        except:
            raise HTTPError(400)

        if self.mongo.categories.find({'_id':cid}).count() == 0:
            raise HTTPError(400)
            
        tags = self.get_argument('tags')
        tags = [i.strip() for i in tags.split(',')]
            
        if len(title) == 0:
            self.redirect('/')
            return

        tid = self.mongo.threads.insert({'title':title,
                                         'author':self.user['_id'],
                                         'datetime':now,
                                         'lastreply':now,
                                         'category':cid,
                                         'hidden':False,
                                         'tags':tags})
        
        self.mongo.posts.insert({'author':self.user['_id'],
                                 'datetime':now,
                                 'th':tid,
                                 'hidden':False,
                                 'content':content})

        self.redirect('/thread/view/%s'%str(tid))
