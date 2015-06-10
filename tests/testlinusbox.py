__author__ = 'Alex H Wagner'

from gmstk.linusbox import *

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
        pass
        # copy the test file

    def e_scp_put_test(self):
        pass
