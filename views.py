from string import Template
import cyan

# page content: just a string
welcome_page = '''
<html>
<head>$head</head>
<body>
    <h1>Hello $name!</h1>
    <p>How are you?</p>
</body>
</html>
'''

def hello_cyan(environ, start_response):
    urlreq = environ['PATH_INFO']
    tokens = cyan.urlparse(urlreq)
    
    totalnum = len(tokens)

    status = '200 OK'
    headers = [('Content-type', 'text/html; charset=utf-8')]
    start_response(status, headers)
    
    temp = Template(welcome_page)
    #customized_content = [temp.substitute (head = len(item), name = item) for item in tokens if (item != '')]
    reqname = tokens[totalnum-1]
    customized_content = temp.substitute(head = len(reqname), name = reqname)
    return [customized_content.encode("utf-8")]

if __name__=='__main__':
    cyan.route('/hello_cyan/', hello_cyan)
    cyan.runapp('localhost',8000,hello_cyan)
