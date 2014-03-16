#!/usr/bin/env python3.3
from tornado.template import Loader

l = Loader("templates")

static_pages = [
    "new.html"
]

print("Generating Static Pages...")

for i in static_pages:
    content = l.load(i).generate()
    with open("static/html/" + i,"wb") as f:
        f.write(content)

print("Generating Error Pages....")
e404 = l.load("404.html").generate()
e50x = l.load("50x.html").generate()

with open("static/html/404.html","wb") as f:
    f.write(e404)

with open("static/html/50x.html","wb") as f:
    f.write(e50x)
