from Fujiwara.handlers.base import Base
from Fujiwara.handlers.thread_view import RenderThread
from Fujiwara.handlers.list import ListByTag,ListAllThread,ListAllTags,ListDeleted,ListByCategory
from Fujiwara.handlers.edit import EditPost,EditThread
from Fujiwara.handlers.join import Join
from Fujiwara.handlers.login import Login
from Fujiwara.handlers.logout import Logout
from Fujiwara.handlers.new import New
from Fujiwara.handlers.reply import Reply
from Fujiwara.handlers.user import User,ReplyNotifications
from Fujiwara.handlers.remove import RemovePost,RemoveThread
from Fujiwara.handlers.recovery import RecoverPost,RecoverThread
from Fujiwara.handlers.categories import ListCategories,AddCategory

handlers = [('/new',New),
            ('/join',Join),
            ('/login',Login),
            ('/logout',Logout),
            ('/reply/(.*)',Reply),
            ('/',ListAllThread),
            ('/categories',ListCategories),
            ('/categories/new',AddCategory),
            ('/category/(.*)/*(\d*)',ListByCategory),
            ('/user',User),
            ('/user/reply/*([0-9]*)',ReplyNotifications),
            ('/thread/remove/(.*)',RemoveThread),
            ('/post/remove/(.*)',RemovePost),
            ('/thread/recover/(.*)',RecoverThread),
            ('/post/recover/(.*)',RecoverPost),
            ('/deleted/*(\d*)',ListDeleted),
            ('/tags/{0,1}(\d*)',ListAllTags),
            ('/tag/([^/]*)/{0,1}(\d*)',ListByTag),
            ('/all/{0,1}(\d*)',ListAllThread),
            ('/post/edit/([0-9A-Za-z]+)',EditPost),
            ('/thread/edit/([0-9A-Za-z]+)',EditThread),
            ('/thread/view/([0-9A-Za-z]+)/{0,1}([0-9]*)',RenderThread)]
