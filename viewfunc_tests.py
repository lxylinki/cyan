# This is for view functions
import subprocess
import random
from jinja2 import Template
import string
import constants
import unittest
import views

class TestViewFuncs(unittest.TestCase):
    
    def test_welcomepage(self):
        devcyan = 'http://localhost:20143/hello_cyan/'
        testfunc = ''.join([ random.choice(string.ascii_letters) for _ in range(10) ])
        devcyan_addr = ''.join([devcyan, testfunc])
        print (devcyan_addr)
        curlout = subprocess.check_output(['curl', devcyan_addr],universal_newlines = True)
        funcout = views.hello_cyan(testfunc)
        self.assertEqual(curlout, funcout)

    def test_exitpage(self):
        devcyan = 'http://localhost:20143/seeyou_cyan/'
        testfunc = ''.join([ random.choice(string.ascii_letters) for _ in range(10) ])
        devcyan_addr = ''.join([devcyan, testfunc])
        print (devcyan_addr)
        curlout = subprocess.check_output(['curl', devcyan_addr],universal_newlines = True)
        funcout = views.seeyou_cyan(testfunc)
        self.assertEqual(curlout, funcout)

    def test_errorpage(self):
        devcyan = 'http://localhost:20143/'
        testfunc = ''.join([ random.choice(string.ascii_letters) for _ in range(10) ])
        devcyan_addr = ''.join([devcyan, testfunc])
        print (devcyan_addr)
        temp = Template(views.error)
        funcout = temp.render(url = testfunc)
        curlout = subprocess.check_output(['curl', devcyan_addr],universal_newlines = True)
        self.assertEqual(curlout, funcout)



if __name__=='__main__':
    unittest.main()
