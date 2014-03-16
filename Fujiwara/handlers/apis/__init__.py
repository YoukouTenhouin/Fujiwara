from Fujiwara.handlers.apis.base import ApiBase
from Fujiwara.handlers.apis.register import Register
from Fujiwara.handlers.apis.userinfo import UserInfo
from Fujiwara.handlers.apis.account import Login,Logout
from Fujiwara.handlers.apis.threads import ThreadAdd,ThreadDel,ThreadUpdate
from Fujiwara.handlers.apis.posts import PostAdd,PostDel,PostUpdate

handlers = [
    ('/api/user/info',UserInfo),
    ('/api/user/login',Login),
    ('/api/user/logout',Logout),
    ('/api/user/register',Register),
    ('/api/thread/add',ThreadAdd),
    ('/api/thread/del',ThreadDel),
    ('/api/thread/update',ThreadUpdate),
    ('/api/post/add',PostAdd),
    ('/api/post/del',PostDel),
    ('/api/post/update',PostUpdate)
]
