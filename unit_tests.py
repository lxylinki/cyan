import string
import unittest
import random
import cyan

class TestUrlFuncs(unittest.TestCase):

    def test_route(self):
        testurl = ''.join( [ random.choice(string.ascii_letters) for _ in range(10) ] )
        testfunc = ''.join( [ random.choice(string.ascii_letters) for _ in range(10) ] )
        fullreq = '/'.join([testurl, testfunc])
        print ("full request %s\n" % fullreq)
        cyan.route( testurl, testfunc)
        self.assertTrue( testurl in cyan.routing_table )
        self.assertEqual( cyan.routing_table[testurl], testfunc)

    def test_urlparse(self):
        testurl = ''.join( [ random.choice(string.ascii_letters) for _ in range(10) ] )
        testfunc = ''.join( [ random.choice(string.ascii_letters) for _ in range(10) ] )
        fullreq = '/'.join([testurl, testfunc])
        print ("full request %s\n" % fullreq)
        
        tokens = cyan.urlparse(fullreq)
        num = len(tokens)
        self.assertEqual( tokens[0], testurl)
        self.assertEqual( tokens[num-1], testfunc)

    def test_find_path(self):
        testurl = ''.join( [ random.choice(string.ascii_letters) for _ in range(10) ] )
        testfunc = ''.join( [ random.choice(string.ascii_letters) for _ in range(10) ] )
        fullreq = '/'.join([testurl, testfunc])
        print ("full request %s\n" % fullreq)
        cyan.route(testurl, testfunc)
        self.assertEqual(cyan.find_path(testurl), testfunc)
        error_url = 'wrongurl'
        self.assertFalse(cyan.find_path(error_url))

if __name__=='__main__':
    unittest.main()
