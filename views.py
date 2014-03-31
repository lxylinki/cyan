from string import Template
import cyan

# page content: just a string
welcome_page = '''
<html>
<head>$head</head>
<body>
    <h1>Hello $name! How are you?</h1>
    <p>Happy browsing.</p>
</body>
</html>
'''
exit_page = '''
<html>
<head>$head</head>
<body>
    <h1>$name, thank you for visiting! Goodbye.</h1>
    <p> An app developed on cyan framework</p>
</body>
</html>
'''
error_page = '''
<html>
<head>ERROR</head>
<body>
    <h1>An error occurred!</h1>
    <p>Your requested $url is not here.</p>
    <p>Please try to enter another url.</p>
</body>
</html>
'''

# functions for devcyan app
#TODO: input a list of parameters
def hello_cyan(reqname):
    temp = Template(welcome_page)
    return temp.substitute(head = len(reqname), name = reqname)

def seeyou_cyan(reqname):
    temp = Template(exit_page)
    return temp.substitute(head = len(reqname), name = reqname)

# devcyan is the app
def devcyan(environ, start_response):
    urlreq = environ['PATH_INFO']
    tokens = cyan.urlparse(urlreq)
    totalnum = len(tokens)
    
    headers = [('Content-type', 'text/html; charset=utf-8')]
    
    # token[0] is empty string ''
    static_url = tokens[1];
    myfunc = cyan.find_path(static_url)
    
    # check if tokens valid i.e. in the routing table
    if( myfunc == None ):
        status = '500 not OK'
        start_response(status, headers)
        temp = Template(error_page)
        error_msg = temp.substitute(url = static_url)
        return [error_msg.encode('utf-8')]
    else:
        dyn_param = tokens[totalnum-1]
        args = [dyn_param]
        status = '200 OK'
        start_response(status, headers)
        page_content = myfunc(*args)
        return [page_content.encode('utf-8')]



if __name__=='__main__':
    cyan.route('hello_cyan', hello_cyan)
    cyan.route('seeyou_cyan', seeyou_cyan)
    cyan.runapp('localhost', 20143, devcyan)
