# constants, templates, etc.
from jinja2 import Template
PORT_NUM = 20143

# max number of tokens in url request
max_tokennum  = 3

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

login= '''
<!DOCTYPE HTML>
<html>
<head>
    <Title>Cyan</title>
</head>
<body>
</h1>Login</h1>
    <form method="POST" action={{redirect}} >
        <dl>
            <dt>Username: 
            <dd><input type=text name=username>
            <dt>Password: 
            <dd><input type=password name=password>
            <dd><input type=submit value=Submit>
        </dl>
    </form>
</body>
</html>
'''

