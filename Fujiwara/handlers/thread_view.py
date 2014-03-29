import tornado.web

from Fujiwara.handlers import Base
from bson.objectid import ObjectId
from bson.errors import InvalidId

POST_PER_PAGE = 30

class RenderThread(Base):
    def get(self,tid,page):
        try:
            if page == '':
                page = 1
            else:
                page = int(page)
        except:
            raise tornado.web.HTTPError(404)

        try:
            tid = ObjectId(tid)
        except InvalidId:
            raise tornado.web.HTTPError(404)
            
        res = self.mongo.threads.find({'_id':tid})
        
        if res.count() == 0:
            raise tornado.web.HTTPError(404)

        thread = res[0]
        if thread['hidden'] and self.user != None and 'admin' not in self.user['jobs']:
            raise tornado.HTTPError(404)

        if self.user!= None and 'admin' in self.user['jobs']:
            posts = self.mongo.posts.find({'th':tid}).sort([('datetime',1)])
        else:
            posts = self.mongo.posts.find({'th':tid,'hidden':False}).sort([('datetime',1)])

        max_pn = (posts.count() - 1)//POST_PER_PAGE + 1
        print(max_pn)
        if max_pn != 0 and page > max_pn:
            raise tornado.web.HTTPError(404)

        skips = (page-1)*POST_PER_PAGE

        posts = posts.skip(skips).limit(POST_PER_PAGE)

        self.render('thread_view.html',
                    thread = thread,
                    posts = posts,
                    pn = page,
                    max_pn = max_pn,
        )
