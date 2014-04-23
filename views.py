# views: user code goes here
from jinja2 import Template
import constants
import cyan

welcomepage = Template(constants.hey)
exitpage = Template(constants.bye)
errorpage = Template(constants.error)

# functions for devcyan app
def cyan_login(reqname):
    pass

def hello_cyan(reqname):
    return welcomepage.render(name1 = reqname, name_list = ['John Doe', 'Jane Doe', 'Joe Doe', 'Janice Doe'])

def seeyou_cyan(reqname):
   return exitpage.render(name2 = reqname, bye_list = ['German: Auf Wiedersehen', 'French: au revoir', 'Italian: arrivederci', 'Swahili: kwa heri'])

def error_page(reqname):
    return errorpage.render(url = reqname)

def devcyan(url_request, routing_table):
    
    # get function from url_request
    myfunc = cyan.url_func(url_request, routing_table)

    if myfunc == None:
        error_msg = error_page(myfunc)
        return [error_msg.encode('utf-8')]
    else:
        # get argument for your function
        arg = cyan.url_arg(url_request)
        page_content = myfunc(arg)
        return [page_content.encode('utf-8')]


if __name__=='__main__':
    
    # return an instance of appinfo
    myapp = cyan.app('devcyan')
    
    # route functions for the app
    myapp.route('hello_cyan', hello_cyan) 
    myapp.route('seeyou_cyan', seeyou_cyan )
    myapp.route('error_page', error_page )
    
    # run the application
    myapp.run()
