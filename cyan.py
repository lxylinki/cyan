from wsgiref.simple_server import WSGIServer
from wsgiref.simple_server import make_server
from http import cookies
import re
import uuid
import redis
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
    
    def route(self, url, func ):
        self.routing_table[url]=func
    
    def run( self, ip='0.0.0.0', port=constants.PORT_NUM ):
        
        def app_wrapper( environ, start_response ):
            myapp = getattr(views, "%s" %self.appname)
            clientIP = environ['REMOTE_ADDR']

            # generate a cookie need to encode it to string
            mycookie = cookie_gen(clientIP)
            headers = [('Content-type','text/html; charset=utf-8'),
                    mycookie.value_encode(mycookie)]
            status = '200 OK'
            if myapp == None:
                status = '500 ERROR'
            
            # redis db connection
            mypool = redis.ConnectionPool(host="localhost", port=6379, db=0)
            setKeyVal( str(mycookie[clientIP]), clientIP, mypool) 
            
            start_response(status, headers)
            return myapp(environ['PATH_INFO'], self.routing_table)
        
        myserver = make_server(ip, port, app_wrapper)
        print("Cyan wsgi server at http://%s:%s" % (ip, port))
        myserver.serve_forever()

# session info
class login_session():
    def __init__(self, usrip, session_id):
        self.ip = usrip
        self.id = session_id

    def get_usrip():
        return self.usrip

    def get_sessionid():
        return self.id


# user info
class user():
    def __init__(self, name, passwd):
        self.name = name
        self.passwd = passwd

    def get_usrname():
        return self.name

# for interaction with redis
def getVal(key, conn_pool):
    myserver = redis.Redis(connection_pool=conn_pool)
    resp = myserver.get(key)
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

