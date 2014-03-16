from tornado.ioloop import IOLoop
from tornado.process import fork_processes,cpu_count
from tornado.options import define,parse_command_line,options
from tornado.tcpserver import bind_sockets
from tornado.httpserver import HTTPServer

from Fujiwara import Application

if __name__ == '__main__':
    define('port',type=int,default=8080)
    define('key',type=str)
    parse_command_line()

    socks = bind_sockets(options.port)

    fork_processes(cpu_count()+1)

    app = Application(options.key)
        
    server = HTTPServer(app)
    server.add_sockets(socks)
    
    IOLoop.instance().start()
