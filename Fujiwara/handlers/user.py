import tornado.web

from Fujiwara.handlers.base import Base
from Fujiwara.decorators import login_requested

from bson.objectid import ObjectId

REPLY_PER_PAGE=30

class User(Base):
    @login_requested
    def get(self):
        self.render('user.html',
                    pagetitle=self.user['name'])

class ReplyNotifications(Base):
    @login_requested
    def get(self,page):
        user = self.user
        if page == '':
            page = 1
        else:
            page = int(page)
            
        posts = self.mongo.posts.find({
            'author':{'$ne':user['_id']},
            'replyto':user['_id'],
            'hidden':{'$ne':True},
        }).sort([('datetime',-1)])

        count = posts.count()

        skips = REPLY_PER_PAGE*(page - 1)
        max_pn = (count-1)//REPLY_PER_PAGE + 1
        
        posts = [i for i in posts.skip(skips).limit(REPLY_PER_PAGE)]
        
        tids = set([i['th'] for i in posts])
        aids = set([i['author'] for i in posts])
        threads = {}
        authors = {}
        for i in tids:
            threads[i] = self.mongo.threads.find({'_id':i})[0]
            
        for i in aids:
            authors[i] = self.mongo.users.find({'_id':i})[0]

        notifications = [(threads[i['th']],i,authors[i['author']]) for i in posts]
            
        self.render('replyto.html',
                    pn = page,
                    max_pn = max_pn,
                    notifications=notifications,
                    pagetitle="Reply Notifications"
                )

handlers = [
    ('/user',User),
    ('/user/reply/*([0-9]*)',ReplyNotifications)
]
