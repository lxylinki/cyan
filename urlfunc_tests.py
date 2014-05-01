# This is for url functions  

import unittest
import string
import random
import cyan

class TestData:
    def __init__(self):
        self.testurl = ''.join( [ random.choice(string.ascii_letters) for _ in range(10) ] )
        self.testfunc = ''.join( [ random.choice(string.ascii_letters) for _ in range(10) ] )
        self.fullreq = '/'.join( [ self.testurl, self.testfunc] )
        self.erroreq = '/'.join( [ self.testfunc, self.testfunc, self.testfunc] )

class TestUrlFuncs(unittest.TestCase):

    def test_route(self):
        testapp = cyan.app('routetest')
        data = TestData()
        print ("url route test %s\n" % data.fullreq)
        testapp.route(data.testurl, data.testfunc )
        self.assertTrue(data.testurl in testapp.routing_table)
        self.assertEqual(testapp.routing_table[data.testurl], data.testfunc)

    def test_urlparse(self):
        testapp = cyan.app('urlparsetest')
        data = TestData()
        print ("url parse test %s\n" % data.fullreq)
        tokens = cyan.urlparse(data.fullreq)
        self.assertTrue(tokens[0], data.testurl)
        self.assertTrue(tokens[len(tokens)-1], data.testfunc)


    def test_url_func(self):
        testapp = cyan.app('urlfunctest')
        data = TestData()
        print ("url func test %s\n" % data.fullreq)
        print ("url func test error case %s\n" % data.erroreq)
        testapp.route(data.testurl, data.testurl)
        self.assertFalse(cyan.url_func(data.erroreq, testapp.routing_table))
        self.assertEqual(cyan.url_func(data.fullreq, testapp.routing_table), data.testurl)


    def test_url_arg(self):
        testapp = cyan.app('urlargtest')
        data = TestData()
        print ("url arg test %s\n" % data.fullreq)
        self.assertEqual(cyan.url_arg(data.fullreq), data.testfunc)
        

if __name__=='__main__':
    unittest.main()
