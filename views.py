# views: user code goes here
from jinja2 import Template
import constants
import cyan

loginpage = Template(constants.login)
welcomepage = Template(constants.hey)
exitpage = Template(constants.bye)
errorpage = Template(constants.error)

# functions for devcyan app, need reqname as argument by default
# set reqname to None if not required

# this is my auth func
# name and authresult will back from framework side 
def cyan_login( reqname=None, name='', authresult=False):
    if authresult == False:
        return loginpage.render(redirect='/cyan_login')

    login_url='/hello_cyan/'+name
    return loginpage.render(redirect=login_url)

# regular funcs
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
        return error_msg
    else:
        # get argument for your function
        arg = cyan.url_arg(url_request)
        return myfunc(arg)

if __name__=='__main__':
    # return an instance of appinfo
    myapp = cyan.app('devcyan')
    
    # route functions for the app
    myapp.route('/', cyan_login )
    myapp.route('/cyan_login', cyan_login )
    myapp.route('/hello_cyan', hello_cyan) 
    myapp.route('/seeyou_cyan', seeyou_cyan )
    myapp.route('/error_page', error_page )
    
    # run the application
    myapp.run()
    #myapp.run(auth=True, authfunc='cyan_login')
