from tornado.httpclient import AsyncHTTPClient,HTTPRequest
from tornado.httputil import urlencode
from tornado.gen import coroutine

def logind(not_logind_response={'success':False,'error':1}):
    def decorator(func):
        def ret(self,*args,**kwargs):
            cookie = self.get_cookie('userinfo',None)
            if not self.auth.vaild(cookie):
                self.clear_cookie('userinfo')
                try:
                    response = not_logind_response(self)
                except:
                    response = not_logind_response
                self.write(response)
                return
            else:
                uid = self.auth.decodeData(cookie)['uid']
                user = self.mongo.users.find({'_id':uid})[0]
                func(self,user=user,*args,**kwargs)
         # Function ret end       
        return ret
        # Function decorator end
    return decorator

def check_recaptcha(func):
    @coroutine
    def ret(self,*args,**kwargs):
        response_field = self.get_argument('recaptcha_response_field')
        challenge_field = self.get_argument('recaptcha_challenge_field')
        privatekey = self.settings['recaptcha_privkey']
        remote_ip = self.request.remote_ip

        postdata = {
            'privatekey':privatekey,
            'challenge':challenge_field,
            'response':response_field,
            'remoteip':remote_ip
        }

                
        request = HTTPRequest(
            "http://www.google.com/recaptcha/api/verify",
            method="POST",
            body=urlencode(postdata)
        )

        client = AsyncHTTPClient()
        response = yield client.fetch(request)
        
        if not response.error:
            [true_or_false,_] = response.body.decode().split('\n',1)
            true_or_false = true_or_false.strip()
            func(self,captcha=(true_or_false == "true"),
                 *args,**kwargs)
        else:
            pass
        
    # Function ret end
    
    return ret
