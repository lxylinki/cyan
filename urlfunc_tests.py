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
        info = cyan.appinfo('routetest')
        data = TestData()
        print ("url route test %s\n" % data.fullreq)
        cyan.route(data.testurl, data.testfunc, info.routing_table)
        self.assertTrue(data.testurl in info.routing_table)
        self.assertEqual(info.routing_table[data.testurl], data.testfunc)

    def test_urlparse(self):
        info = cyan.appinfo('urlparsetest')
        data = TestData()
        print ("url parse test %s\n" % data.fullreq)
        tokens = cyan.urlparse(data.fullreq)
        self.assertTrue(tokens[0], data.testurl)
        self.assertTrue(tokens[len(tokens)-1], data.testfunc)


    def test_url_func(self):
        info = cyan.appinfo('urlfunctest')
        data = TestData()
        print ("url func test %s\n" % data.fullreq)
        print ("url func test error case %s\n" % data.erroreq)
        cyan.route(data.testurl, data.testurl, info.routing_table)
        self.assertFalse(cyan.url_func(data.erroreq, info.routing_table))
        self.assertEqual(cyan.url_func(data.fullreq, info.routing_table), data.testurl)


    def test_url_arg(self):
        info = cyan.appinfo('urlargtest')
        data = TestData()
        print ("url arg test %s\n" % data.fullreq)
        self.assertEqual(cyan.url_arg(data.fullreq), data.testfunc)
        

if __name__=='__main__':
    unittest.main()
