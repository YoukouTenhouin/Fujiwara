import tornado.web

from Fujiwara.handlers.views import ViewBase
from bson.objectid import ObjectId

class EditPost(ViewBase):
    def get(self,pid):
        res = self.mongo.posts.find({'_id':ObjectId(pid)})
        if res.count() == 0:
            raise tornado.web.HTTPError(404)

        self.render('edit.html',post = res[0],edit_thread=False)

class EditThread(ViewBase):
    def get(self,tid):
        res = self.mongo.threads.find({'_id':ObjectId(tid)})
        if res.count() == 0:
            raise tornado.web.HTTPError(404)

        thread = res[0]
        first_post = self.mongo.posts.find({'th':ObjectId(tid)})[0]

        self.render('edit.html',
                    post = first_post,
                    thread = thread,edit_thread = True)
