import tornado.web

from Fujiwara.handlers.views.base import ViewBase

TAG_PER_PAGE = 100
THREAD_PER_PAGE = 30

class ListAllThread(ViewBase):
    def get(self,page = 1):
        if page == '':
            page = 1
        else:
            page = int(page)
            
        threads = self.mongo.threads.find({'hidden':{'$ne':True}}).sort([('lastreply',-1)])

        max_pn = (threads.count() - 1)//THREAD_PER_PAGE + 1
        if (max_pn != 0) and (page > max_pn):
            raise tornado.web.HTTPError(404)
        
        skips = THREAD_PER_PAGE * (page - 1)

        threads = threads.skip(skips).limit(THREAD_PER_PAGE)
        
        self.render('thread_list.html',
                    threads = threads,
                    pn = page,
                    max_pn = max_pn,
                    tag = None,
                    pager_prefix='/all')

class ListAllTags(ViewBase):
    def get(self,page = 1):
        if page == '':
            page = 1
        else:
            page = int(page)

        tags = self.mongo.threads.find({"hidden":{"$ne":True}}).distinct("tags")
        max_pn = (len(tags) - 1)//TAG_PER_PAGE + 1
        if page > max_pn:
            raise tornado.web.HTTPError(404)

        skips = (page - 1)*TAG_PER_PAGE
        threads = tags[skips:skips+TAG_PER_PAGE]

        self.render('tags.html',
                    tags = tags,
                    pn = page,
                    max_pn = max_pn)

class ListByTag(ViewBase):
    def get(self,tag,page = 1):
        if page == '':
            page = 1
        else:
            page = int(page)
            
        threads = self.mongo.threads.find({'tags':tag,'hidden':{'$ne':True}})
        max_pn = (threads.count() - 1)//THREAD_PER_PAGE + 1

        if page > max_pn:
            raise tornado.web.HTTPError(404)

        skips = (page - 1)*THREAD_PER_PAGE
        threads = threads.skip(skips).limit(THREAD_PER_PAGE)
            
        self.render('thread_list.html',
                    threads = threads,
                    pn = page,
                    max_pn = max_pn,
                    tag = tag,
                    pager_prefix = '/tag/'+tag,)
