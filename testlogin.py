import urllib.parse
import httplib2

http = httplib2.Http()

url = 'http://localhost:20143'
#body = {'username':'myname', 'password':'mypass'}
body = {'username':'myname', 'password':'mypassw'}

#headers = {'Content-type':'application/x-www-form-urlencoded'}
headers = {'Content-type':'text/html; charset=utf-8'}
response, content = http.request(url,'POST', headers = headers, body=urllib.parse.urlencode(body))
headers = {'Cookie':response['set-cookie']}

print (response)
print (content)

