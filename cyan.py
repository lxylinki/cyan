from wsgiref.simple_server import WSGIServer
from wsgiref.simple_server import make_server
from http import cookies
from jinja2 import Template
from cgi import parse_qs, escape

import re
import redis
import string
import random

import views
import constants

# class for your application basic info
class app:
    def __init__(self, name, table={}, sessions={}):
        self.appname = name
        self.routing_table = table
        self.active_sessions = sessions

    def get_appname(self):
        return self.name
    
    def route(self, url, func):
        self.routing_table[url]=func
    
    def run(self, ip='0.0.0.0', port=constants.PORT_NUM, auth=False):
        def auth_wrapper( environ, start_response ):
            # redis db connection pool
            mypool = redis.ConnectionPool(host='localhost', port=6379, db=0) 
            cliIP = environ['REMOTE_ADDR']
            login = False

            # retrive cookie from client
            cliCookie = cookies.SimpleCookie()
            
            # if there no cookie present yet
            if environ.get('HTTP_COOKIE') == None:
                login = False
            else:
                # check if client is valid logged in
                cliCookie.load(environ.get('HTTP_COOKIE'))
                clikey = cliCookie[cliIP].value
                login = authcheck(clikey, cliIP, mypool)
           
            # check if the client is logged in i.e. a cookie is present and mathes our records in redis
            if login == False:
                # generate a cookie need to encode it to string
                mycookie = cookie_gen(cliIP)
                headers = [('Content-type','text/html; charset=utf-8'), tuple(re.split(':', mycookie.output()))]
                setKeyVal( mycookie[cliIP].value, cliIP, mypool) 
            else:
                headers = [('Content-type', 'text/html; charset=utf-8')]
            
            status = '200 OK'
            # app func name
            myapp = getattr(views, "%s" % self.appname)
            if myapp == None:
                status = '500 ERROR'
            start_response(status, headers)
            return myapp(environ['PATH_INFO'], self.routing_table)

        # wrap app with authentication, loginpage is a string template
        def app_wrapper(environ, start_response):
            headers = [('Content-type', 'text/html; charset=utf-8')]
            # app func name
            myapp = getattr(views, "%s" % self.appname)
            status = '200 OK'
            if myapp == None:
                status = '500 ERROR'
            start_response(status, headers)
            return myapp(environ['PATH_INFO'], self.routing_table)
        
        if auth == True:
            myserver = make_server(ip, port, auth_wrapper)
        else:
            myserver = make_server(ip, port, app_wrapper)
        print("Cyan wsgi server at http://%s:%s" % (ip, port))
        myserver.serve_forever()

def authcheck( name, value, conn_pool ):
    validvalue = getVal( name, conn_pool )
    if validvalue == None:
        return False
    if validvalue != value:
        return False
    return True

# session info
class login_session:
    def __init__(self, usrip, session_id):
        self.ip = usrip
        self.id = session_id

    def get_usrip():
        return self.usrip

    def get_sessionid():
        return self.id

# user info
class user:
    def __init__(self, name, passwd):
        self.name = name
        self.passwd = passwd

    def get_usrname():
        return self.name

# for interaction with redis
# return a string value from key
def getVal(key, conn_pool):
    myserver = redis.Redis(connection_pool=conn_pool)
    
    # this is a bytes object
    value = myserver.get(str(key))
    return value.decode('utf-8')

# take key and val as strings
def setKeyVal(key, val, conn_pool):
    myserver = redis.Redis(connection_pool=conn_pool)
    # encode key to utf-8
    myserver.set(str(key), val)

# generate a cookie
def cookie_gen( clientIP, idlen = 8 ):
    c = cookies.SimpleCookie()
    sessionID = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(idlen)])
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

