import tornado.web

from Fujiwara.handlers.base import Base

from bson.objectid import ObjectId

TAG_PER_PAGE = 100
THREAD_PER_PAGE = 30

class ListAllThread(Base):
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
        
        self.render('list.html',
                    pager_prefix='/all',
                    threads = threads,
                    pn = page,
                    max_pn = max_pn)

class ListDeleted(Base):
    def get(self,page = 1):
        if page == '':
            page = 1
        else:
            page = int(page)
            
        threads = self.mongo.threads.find({'hidden':True}).sort([('lastreply',-1)])

        max_pn = (threads.count() - 1)//THREAD_PER_PAGE + 1
        if (max_pn != 0) and (page > max_pn):
            raise tornado.web.HTTPError(404)
        
        skips = THREAD_PER_PAGE * (page - 1)

        threads = threads.skip(skips).limit(THREAD_PER_PAGE)
        
        self.render('list.html',
                    pager_prefix='/deleted',
                    threads = threads,
                    pn = page,
                    max_pn = max_pn)

class ListAllTags(Base):
    def get(self,page = 1):
        if page == '':
            page = 1
        else:
            page = int(page)

        tags = self.mongo.threads.find({"hidden":True}).distinct("tags")
        max_pn = (len(tags) - 1)//TAG_PER_PAGE + 1
        if page > max_pn:
            raise tornado.web.HTTPError(404)

        skips = (page - 1)*TAG_PER_PAGE
        threads = tags[skips:skips+TAG_PER_PAGE]

        self.render('tags.html',
                    pager_prefix='/tags/',
                    tags = tags,
                    pn = page,
                    max_pn = max_pn)

class ListByTag(Base):
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
            
        self.render('list_by_tag.html',
                    threads = threads,
                    pn = page,
                    max_pn = max_pn,
                    tag = tag,
                    pager_prefix = '/tag/'+tag)

class ListByCategory(Base):
    def get(self,cid,page):
        if page == '':
            page = 1
        else:
            page = int(page)
            
        threads = self.mongo.threads.find({'category':ObjectId(cid),'hidden':{'$ne':True}})
        max_pn = (threads.count() - 1)//THREAD_PER_PAGE + 1

        if page > max_pn:
            raise tornado.web.HTTPError(404)

        skips = (page - 1)*THREAD_PER_PAGE
        threads = threads.skip(skips).limit(THREAD_PER_PAGE)
            
        self.render('list_by_category.html',
                    threads = threads,
                    pn = page,
                    max_pn = max_pn,
                    cid = ObjectId(cid),
                    pager_prefix = '/category/'+cid)
