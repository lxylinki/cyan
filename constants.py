# This is the file for all constants, templates, etc.
# page content: just a string
cyan_port = 20143
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
