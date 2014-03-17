from tornado.ioloop import IOLoop
from tornado.process import fork_processes,cpu_count
from tornado.options import define,parse_config_file,options
from tornado.tcpserver import bind_sockets
from tornado.httpserver import HTTPServer

from Fujiwara import Application

if __name__ == '__main__':
    define('port',type=int,default=8080)
    define('key',type=str)
    define('recaptcha_pubkey',type=str)
    define('recaptcha_privkey',type=str)
    parse_config_file('config')

    socks = bind_sockets(options.port)

    fork_processes(cpu_count()+1)

    app = Application(
        key=options.key,
        recaptcha_privkey=options.recaptcha_privkey,
        recaptcha_pubkey=options.recaptcha_pubkey
    )
        
    server = HTTPServer(app)
    server.add_sockets(socks)
    
    IOLoop.instance().start()
