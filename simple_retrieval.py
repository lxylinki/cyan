import httplib2
h = httplib2.Http(".cache")
# The content is the content retrieved from the url. The resp contains all the response headers
#resp, content = h.request("http://bitworking.org/", "GET")
resp, content = h.request("http://localhost:20143/seeyou_cyan/sarah", "GET")
h.add_credentials('xlin','mypassword')
resp, content = h.request("http://localhost:20143/hello_cyan/sarah", "PUT", body="this is text", headers={'content-type':'text/plain'})
