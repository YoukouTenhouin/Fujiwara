import tornado.web

from Fujiwara.handlers import Base
from Fujiwara.decorators import login_requested

from bson.objectid import ObjectId

class EditPost(Base):
    @login_requested
    def get(self,pid):
        res = self.mongo.posts.find({'_id':ObjectId(pid)})
        if res.count() == 0:
            raise tornado.web.HTTPError(404)

        post = res[0]
        if self.user['_id'] != post['author'] and\
           "admin" not in self.user['jobs']:
            raise tornado.web.HTTPError(404)

        thread = self.mongo.threads.find({'_id':post['th']})[0]
        referer = self.request.headers['referer']
            
        self.render('edit.html',post = post,referer=referer,
                    thread = thread,edit_thread=False)
        
    @login_requested
    def post(self,pid):
        res = self.mongo.posts.find({'_id':ObjectId(pid)})
        if res.count() == 0:
            raise tornado.web.HTTPError(404)

        post = res[0]
        if self.user['_id'] != post['author'] and\
           "admin" not in self.user['jobs']:
            raise tornado.web.HTTPError(404)

        cont = self.get_argument('content')
        referer = self.get_argument('referer')
        
        self.mongo.posts.update({'_id':post['_id']},
                           {'$set':{'content':cont}})

        self.redirect(referer+'#'+pid)

class EditThread(Base):
    @login_requested
    def get(self,tid):
        res = self.mongo.threads.find({'_id':ObjectId(tid)})
        if res.count() == 0:
            raise tornado.web.HTTPError(404)

        thread = res[0]

        if thread['author'] != self.user['_id'] and\
           'admin' not in self.user['jobs']:
            raise tornado.web.HTTPError(404)

        referer = self.request.headers['referer']
            
        self.render('edit.html',thread = thread,
                    referer=referer,edit_thread = True)

    @login_requested
    def post(self,tid):
        res = self.mongo.threads.find({'_id':ObjectId(tid)})

        if res.count() == 0:
            raise tornado.web.HTTPError(404)

        thread = res[0]
        if thread['author'] != self.user['_id'] and\
           'admin' not in self.user['jobs']:
            raise tornado.web.HTTPError(404)
        
        new_title = self.get_argument('title').strip()
        new_category = self.get_argument('category')
        
        try:
            new_cid = ObjectId(new_category)
        except:
            raise HTTPError(400)

        if self.mongo.categories.find({'_id':new_cid}).count() == 0:
            raise HTTPError(400)
        new_tags = self.get_argument('tags')
        new_tags = [i.strip() for i in new_tags.split(',')]

        self.mongo.threads.update({'_id':thread['_id']},
                                  {'$set':
                                   {'title':new_title,
                                    'category':new_cid,
                                    'tags':new_tags}})

        self.redirect("/thread/view/%s"%tid)
