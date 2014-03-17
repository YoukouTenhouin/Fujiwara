import tornado.web

from Fujiwara.handlers.base import Base
from bson.objectid import ObjectId

class User(Base):
    def get(self):
        cookie = self.get_cookie('userinfo')
        if not self.auth.vaild(cookie):
            self.redirect('/')
            return

        uid = self.auth.decodeData(cookie)['uid']
        user = self.mongo.users.find({'_id':uid})[0]
        
        self.render('user.html',
                    user=user,
                    pagetitle=user['name'])

class ReplyNotifications(Base):
    def get(self,page = 1):
        if page == '':
            page = 1
        else:
            page = int(page)
            
        cookie = self.get_cookie('userinfo')
        if not self.auth.vaild(cookie):
            self.redirect('/')
            return

        uid = self.auth.decodeData(cookie)['uid']
        user = self.mongo.users.find({'_id':uid})[0]

        posts = [i for i in self.mongo.posts.find({
            'author':{'$ne':uid},
            'replyto':uid,
            'hidden':{'$ne':True}
        })]
        
        count = len(posts)
        
        skips = 10*(page - 1)
        max_pn = (count-1)//10 + 1

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
                    user=user,
                    pn = page,
                    max_pn = max_pn,
                    notifications=notifications,
                    pagetitle="Reply Notifications"
                )

handlers = [
    ('/user',User),
    ('/user/reply',ReplyNotifications),
    ('/user/reply/([0-9]+)',ReplyNotifications)
]
