__author__ = 'Alex H Wagner'

from gmstk.linusbox import *
import os

def enquote(string):
    return "'" + string + "'"

class TestLinusBox:

    test_dir = 'oh no/'

    @classmethod
    def setup_class(cls):
        cls.linus = LinusBox()
        cls.linus.connect()

    @classmethod
    def teardown_class(cls):
        cls.linus.cd()
        cls.linus.rm('-rf', enquote(cls.test_dir))
        cls.linus.disconnect()
        os.remove('test2.txt')

    def a_mkdir_test(self):
        # make a test dir
        self.linus.mkdir(enquote(self.test_dir))
        r = self.linus.ls()
        assert self.test_dir in r.stdout, 'r is {0}'.format(r.stdout)

    def b_cd_test(self):
        # cd to test dir
        self.linus.cd(enquote(self.test_dir))
        r = self.linus.ls()
        assert r.stdout == ['./', '../'], 'r is {0}'.format(r.stdout)

    def c_touch_test(self):
        # make a test file
        self.linus.touch('test.txt')
        r = self.linus.ls()
        assert 'test.txt' in r.stdout, 'r is {0}'.format(r.stdout)

    def d_scp_get_test(self):
        # copy the test file to local
        self.linus.scp_get('test.txt', 'test2.txt')
        assert os.path.isfile('test2.txt')

    def e_scp_put_test(self):
        #
        self.linus.scp_put('test2.txt')
        r = self.linus.ls()
        assert 'test2.txt' in r.stdout, 'r is {0}'.format(r.stdout)