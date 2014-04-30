from wsgiref.simple_server import WSGIServer
from wsgiref.simple_server import make_server
from http import cookies
from jinja2 import Template
from cgi import parse_qs, escape

import re
import uuid
import redis
import views
import constants


# class for your application basic info
class app:
    # used if auth is required
    loginpage = Template(constants.login)
    
    def __init__(self, name, table={}, sessions={}):
        self.appname = name
        self.routing_table = table
        self.active_sessions = sessions

    def get_appname(self):
        return self.name
    
    def route(self, url, func):
        self.routing_table[url]=func

    def auth(self, usrname, passwd, conn_pool):
        validpasswd = getVal(usrname, conn_pool)
        if validpasswd == None:
            return False
        if passwd != validpass:
            return False
        return True
    
    def run( self, ip='0.0.0.0', port=constants.PORT_NUM ):
        
        def app_wrapper( environ, start_response ):
            usrname = 'testkey'
            password = 'testval'
            
            # redis db connection
            mypool = redis.ConnectionPool(host="localhost", port=6379, db=0)
            
            # display login page
            status = '200 OK'
            headers = [('Content-type','text/html; charset=utf-8')]
            start_response(status, headers)
            return (self.loginpage.render()).encode('utf-8')
            
            # while auth is not passed, repeat
            while(self.auth(usrname, password, mypool) == False):
                # extract user post
                try:
                    request_body_size = int(environ.get('CONTENT_LENGTH',0))
                except(ValueError):
                    request_body_size = 0
            
                # this is bytes object
                request_body = environ['wsgi.input'].read(request_body_size)
                req_dict = parse_qs(request_body)
                
                usrname = req_dict.get('username')
                password = req_dict.get('password')
                return (self.loginpage.render()).encode('utf-8')
                # continue exec following code if passed

            # app func name
            myapp = getattr(views, "%s" % self.appname)
            clientIP = environ['REMOTE_ADDR']
            
            # generate a cookie need to encode it to string
            mycookie = cookie_gen(clientIP)
            headers = [('Content-type','text/html; charset=utf-8'),
                    mycookie.value_encode(mycookie)]
            status = '200 OK'

            if myapp == None:
                 status = '500 ERROR'
            
            setKeyVal( str(mycookie[clientIP]), clientIP, mypool) 
            start_response(status, headers)
            return myapp(environ['PATH_INFO'], self.routing_table)
        
        myserver = make_server(ip, port, app_wrapper)
        print("Cyan wsgi server at http://%s:%s" % (ip, port))
        myserver.serve_forever()

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
def getVal(key, conn_pool):
    myserver = redis.Redis(connection_pool=conn_pool)
    value = myserver.get(key)
    return value

def setKeyVal(key, val, conn_pool):
    myserver = redis.Redis(connection_pool=conn_pool)
    myserver.set(key, val)

# generate a cookie
def cookie_gen( clientIP ):
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

