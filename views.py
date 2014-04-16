# views: user code goes here
from jinja2 import Template
import constants
import cyan

welcomepage = Template(constants.hey)
exitpage = Template(constants.bye)
errorpage = Template(constants.error)

# functions for devcyan app
def hello_cyan(reqname):
    return welcomepage.render(name1 = reqname, name_list = ['John Doe', 'Jane Doe', 'Joe Doe', 'Janice Doe'])

def seeyou_cyan(reqname):
   return exitpage.render(name2 = reqname, bye_list = ['German: Auf Wiedersehen', 'French: au revoir', 'Italian: arrivederci', 'Swahili: kwa heri'])

def error_page(reqname):
    return errorpage.render(url = reqname)

# devcyan is the major function in this app
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
    # init appinfo
    myapp = cyan.appinfo('devcyan')
    myroutes = myapp.routing_table
    
    # route functions for the app
    cyan.route('hello_cyan', hello_cyan, myroutes ) 
    cyan.route('seeyou_cyan', seeyou_cyan, myroutes )
    
    # run the application
    cyan.runapp(myapp)
