from wsgiref.simple_server import make_server
import os
import re

routing_table = {}

# url convention: /func/parameters i.e /func/p0/p1/... 
# or /static/filename
# call views.func(parameters)

def route(url, func):
    routing_table[url] = func

def urlparse(url_request):
    tokens = re.split('\W+', url_request)
    return tokens

def find_path(url):
    if url in routing_table:
        return routing_table[url]
    else:
        return None

def runapp(ip, port, app):
    myserver = make_server(ip, port, app)
    print("Cyan wsgi server at http://%s:%s" % (ip, port))
    myserver.serve_forever()
