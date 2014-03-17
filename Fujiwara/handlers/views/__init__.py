from Fujiwara.handlers.views.base import ViewBase
from Fujiwara.handlers.views.thread_render import RenderThread
from Fujiwara.handlers.views.list import ListByTag,ListAllThread,ListAllTags
from Fujiwara.handlers.views.edit import EditPost,EditThread
from Fujiwara.handlers.views.join import Join

handlers = [('/',ListAllThread),
            ('/all/{0,1}(\d*)',ListAllThread),
            ('/tags/{0,1}(\d*)',ListAllTags),
            ('/tag/([^/]*)/{0,1}(\d*)',ListByTag),
            ('/join',Join),
            ('/post/edit/([0-9A-Za-z]+)',EditPost),
            ('/thread/edit/([0-9A-Za-z]+)',EditThread),
            ('/thread/view/([0-9A-Za-z]+)/{0,1}([0-9]*)',RenderThread)]
