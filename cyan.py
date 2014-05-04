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
        # keep track of users currently logged in
        self.active_sessions = sessions

    def get_appname(self):
        return self.appname
    
    def route(self, url, func):
        self.routing_table[url]=func
    
    def run(self, ip='0.0.0.0', port=constants.PORT_NUM, auth=False, authfunc=None):
        
        def app_wrapper(environ, start_response):
            headers = [('Content-type', 'text/html; charset=utf-8')]
            # app func name
            myapp = getattr(views, "%s" % self.appname)
            status = '200 OK'
            if myapp == None:
                status = '500 ERROR'
            start_response(status, headers)
            return myapp(environ['PATH_INFO'], self.routing_table)
       

        def auth_wrapper( environ, start_response ):
            # redis db connection pool
            mypool = redis.ConnectionPool(host='localhost', port=6379, db=0) 
            login = False
            cliIP = environ['REMOTE_ADDR']
            
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
           
            if login == False:
                # generate a cookie that valid for entire domain
                mycookie = cookie_gen(cliIP)
                mycookie[cliIP]['path'] = '/'
                setKeyVal( mycookie[cliIP].value, cliIP, mypool) 
                
                # get login function provided by app
                appauth = getattr(views, "%s" % authfunc)
                status = '200 OK'
                if appauth == None:
                    status = '500 ERROR'

                # extract username and password, it depends on environ 
                def login_func(reqname=None, reqmethod='POST'):
                    nonlocal appauth, mypool
                    if reqmethod == 'GET':
                        return appauth(None, username, authresult)
                    
                    try:
                        req_body_len = int (environ['CONTENT_LENGTH'])
                    except (ValueError):
                        req_body_len = 0
                    
                    try:
                        req_body = environ['wsgi.input'].read(req_body_len)
                    except (ValueError):
                        req_body = b''
                        
                    req_dict = parse_qs(req_body)
                    
                    username = (req_dict.get('username'.encode('utf-8'))[0]).decode('utf-8')
                    password = (req_dict.get('password'.encode('utf-8'))[0]).decode('utf-8')
                
                    authresult = authcheck(username, password, mypool)
                    
                    args = [None, username +','+str(authresult), authresult]
                    return appauth(*args)
               
                # add this login func to app routes
                self.route( ('/' + authfunc), login_func )
                page_content = login_func( authfunc, environ['REQUEST_METHOD'] )
                
                headers = [('Content-type','text/html; charset=utf-8'), 
                        ('Content-Length', str(len(page_content))), 
                        tuple(re.split(':', mycookie.output()))]
                
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
    if value != None:
        return value.decode('utf-8')
    return value

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


# url manipulation funcs
def urljoin(func, arg):
    return '/'.join([func, arg])


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

