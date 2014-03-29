#!/usr/bin/env python3.3
from tornado.template import Loader

l = Loader("templates")

print("Generating Error Pages....")
e404 = l.load("404.html").generate(user=None)
e50x = l.load("50x.html").generate(user=None)

with open("static/html/404.html","wb") as f:
    f.write(e404)

with open("static/html/50x.html","wb") as f:
    f.write(e50x)
