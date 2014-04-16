from wsgiref.simple_server import WSGIServer
from wsgiref.simple_server import make_server
import inspect
import re

import constants
import views

# class for your application's basic information 
# application name and routing table

class appinfo:
    def __init__(self, name, table={}):
        self.appname = name
        self.routing_table = table

    def get_appname(self):
        return self.name

def route(url, func, routing_table):
    routing_table[url]=func

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


def runapp( appinfo, ip='localhost', port=constants.PORT_NUM ):
    
    def app_wrapper( environ, start_response):
        nonlocal appinfo
        # get app function from views
        myapp = getattr( views, "%s" % appinfo.appname )
        
        headers = [('Content-type','text/html; charset=utf-8')]
        status = '200 OK'
        if myapp == None:
            status = '500 ERROR'
        start_response(status, headers)
        return myapp(environ['PATH_INFO'], appinfo.routing_table) 
    
    myserver = make_server(ip, port, app_wrapper)
    print("Cyan wsgi server at http://%s:%s" % (ip, port))
    myserver.serve_forever()
