from jinja2 import Template
import cyan

# page content: just a string

hey='''
<!DOCTYPE html>
<html>
    <head>
        <title>Cyan</title>
    </head>
    <body>
        <h1> Hello {{name1}}!</h1>
        <p> We also said hello to the following people: </p>
    <ul>
    {% for name in name_list%}
        <li>{{name}}</li>
    {% endfor %}
    </ul>
    </body>
</html>
'''
bye = '''
<!DOCTYPE html>
<html>
    <head>
        <title>Cyan</title>
    </head>
    <body>
        <h1> Goodbye {{name1}}!</h1>
        <p> We can also say goodbye in other languages: </p>
    <ul>
    {% for bye in bye_list%}
        <li>{{bye}}</li>
    {% endfor %}
    </ul>
    </body>
</html>
'''

error='''
<!DOCTYPE html>
<html>
    <head>
        <title>OOPS! Error.</title>
    </head>
    <body>
        <h1> An error occurred!</h1>
        <p> Your requested url ({{url}}) is not here. Try another. </p>
    </body>
</html>
'''

template1 = Template(hey)
template2 = Template(bye)
template3 = Template(error)

# functions for devcyan app
#TODO: input a list of parameters

def hello_cyan(reqname):
    return template1.render(name1 = reqname, name_list = ['John Doe', 'Jane Doe', 'Joe Doe', 'Janice Doe'])

def seeyou_cyan(reqname):
   return template2.render(name1= reqname, bye_list = ['German: Auf Wiedersehen', 'French: au revoir', 'Italian: arrivederci', 'Swahili: kwa heri'])

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
        error_msg = template3.render(url = static_url)
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
