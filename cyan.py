from wsgiref.simple_server import WSGIServer
from wsgiref.simple_server import make_server

from html import escape
from http import cookies
from jinja2 import Template
from urllib.parse import parse_qs

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
    
    def run(self, ip='0.0.0.0', port=constants.PORT_NUM, auth=False, authfunc=None):
        
        def auth_wrapper( environ, start_response ):
            # redis db connection pool
            mypool = redis.ConnectionPool(host='localhost', port=6379, db=0) 
            cliIP = environ['REMOTE_ADDR']
            login = False
            # if there no cookie present yet
            if environ.get('HTTP_COOKIE') == None:
                pass
            else:
                # retrive cookie from client
                # check if client is valid logged in
                cliCookie = cookies.SimpleCookie()
                cliCookie.load(environ.get('HTTP_COOKIE'))
                clikey = cliCookie[cliIP].value
                login = authcheck(clikey, cliIP, mypool)
           
            # check if the client is logged in i.e. a cookie is present and mathes record
            if login == False:
                # generate a cookie that valid for entire domain
                mycookie = cookie_gen(cliIP)
                mycookie[cliIP]['path'] = '/'
                setKeyVal( mycookie[cliIP].value, cliIP, mypool) 
                
                # get auth function provided by app
                appauth = getattr(views, "%s" % authfunc)
                
                # extract user post info
                ifvalid = authcheck('myname', 'mypasswd', mypool)
                
                # call app auth function with results
                page_content = appauth(name='myname', authresult=ifvalid)
                
                headers = [('Content-type','text/html; charset=utf-8'), 
                        tuple(re.split(':', mycookie.output()))]
                status = '200 OK'
                if authfunc == None:
                    status = '500 ERROR'
                start_response(status, headers)
                return [page_content.encode('utf-8')]
                
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

# match the given name value pair 
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
        self.id = session_id
        self.ip = usrip

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

# when log out delete key from db
def delKey(key, conn_pool):
    myserver = redis.Redis(connection_pool=conn_pool)
    myserver.delete(str(key))

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
    
    url = '' 
    for i in range(len(tokens)):
        if tokens[i]== '':
            continue
        url = tokens[i]
        break
    
    fullurl = ('/'+url).strip()
    if fullurl not in routing_table:
        return None

    return routing_table[fullurl]

def url_arg(url_request):
    tokens = urlparse(url_request)
    num = len(tokens)
    return tokens[num-1] 

