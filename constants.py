# constants, templates, etc.
from jinja2 import Template
PORT_NUM = 20143

# max number of tokens in url request
max_tokennum  = 3

# page content: just a string
login='''
<!DOCTYPE html>
'''
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
        <h1> Goodbye {{name2}}!</h1>
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

testif='''
<!DOCTYPE html>
<html>
    <body>
        <h1>This is my homepage</h1>
        %if name:
    print (Template('My name is $name.').substitute(name = name))
#return (Template('My name is $name.').substitute(name = name))
         #endif%
        
        %if city:
    print (Template('I live in $city.').substitute(city = city))
#return (Template('I live in $city.').substitute(city = city))
         #endif%
    </body>
</html>
'''
