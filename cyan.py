from wsgiref.simple_server import WSGIServer
from wsgiref.simple_server import make_server

import inspect
import re

from http import cookies
import uuid
import constants
import views

# class for your application's basic information 
# application name and routing table

class app:
    def __init__(self, name, table={}):
        self.appname = name
        self.routing_table = table

    def get_appname(self):
        return self.name
    
    def route(self, url, func ):
        self.routing_table[url]=func
    
    def run( self, ip='0.0.0.0', port=constants.PORT_NUM ):
        
        def app_wrapper( environ, start_response):
            myapp = getattr(views, "%s" %self.appname)
            headers = [('Content-type','text/html; charset=utf-8')]
            
            status = '200 OK'
            if myapp == None:
                status = '500 ERROR'

            start_response(status, headers)
            return myapp(environ['PATH_INFO'], self.routing_table)
        
        myserver = make_server(ip, port, app_wrapper)
        print("Cyan wsgi server at http://%s:%s" % (ip, port))
        myserver.serve_forever()

def cookie_gen( clientIP, num_bytes = 12 ):
    c = cookies.SimpleCookie()
    sessionID = uuid.uuid4()
    c[clientIP] = sessionID
    return c


def urlparse(url_request):
    tokens = re.split('\W+', url_request)
    return tokens

def url_func(url_request, routing_table):
    tokens = urlparse(url_request)
    if len(tokens) > constants.max_tokennum:
        return None
    
    for i in range(len(tokens)):
        if tokens[i]== '':
            continue
        url = tokens[i]
        break

    if url not in routing_table:
        return None

    return routing_table[url]

def url_arg(url_request):
    tokens = urlparse(url_request)
    num = len(tokens)
    return tokens[num-1] 

