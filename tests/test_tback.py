#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import sys
import unittest
import re
import six

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # noqa
sys.path.insert(0, PROJECT_DIR)  # noqa

from kobo.tback import Traceback, get_traceback


class TestTraceback(unittest.TestCase):

    def test_empty(self):
        self.assertEqual('', get_traceback())
        self.assertEqual('', Traceback().get_traceback())
        self.assertEqual((None, None, None), Traceback().exc_info)

    def test_text(self):
        try:
            raise Exception('Simple text')
        except:
            regexp = re.compile('Traceback \(most recent call last\):\n *File ".*test_tback.py", line .+, in test_text\n *raise Exception\(\'Simple text\'\)\n *Exception: Simple text', re.M)
            six.assertRegex(self, get_traceback(), regexp)
            tb = Traceback(show_traceback=True, show_code=False, show_locals=False, show_environ=False, show_modules=False)
            six.assertRegex(self, tb.get_traceback(), regexp)

    def test_Traceback(self):
        try:
            raise Exception('Simple text')
        except:
            tb = Traceback(show_traceback=False, show_code=False, show_locals=False, show_environ=False, show_modules=False)
        self.assertEqual('', tb.get_traceback())
        tb.show_code = True
        six.assertRegex(self, tb.get_traceback(), re.compile('<CODE>.*--> *\d+ *raise Exception.*<\/CODE>$', re.M | re.S))
        tb.show_code = False
        tb.show_locals = True
        six.assertRegex(self, tb.get_traceback(), re.compile('<LOCALS>.*tb = .*<\/LOCALS>$', re.M | re.S))
        tb.show_locals = False
        tb.show_environ = True
        six.assertRegex(self, tb.get_traceback(), re.compile('<ENVIRON>.*<\/ENVIRON>\n<GLOBALS>.*</GLOBALS>$', re.M | re.S))
        tb.show_environ = False
        tb.show_modules = True
        six.assertRegex(self, tb.get_traceback(), re.compile('<MODULES>.*<\/MODULES>$', re.M | re.S))

    def test_encoding(self):
        try:
            a = ''.join([chr(i) for i in range(256)])  # noqa
            b = ''.join([chr(i) for i in range(65536)])  # noqa
            raise Exception()
        except:
            tb = Traceback(show_code=False, show_traceback=False)
        output = tb.get_traceback()
        self.assertIsInstance(output, str)

    def test_uninitialized_variables(self):
        class Foo(object):
            __slots__ = ("bar", "version")

            def __init__(self):
                self.version = 1

            def test(self):
                try:
                    raise
                except:
                    # bar is uninitialized
                    return Traceback().get_traceback()

        obj = Foo()
        self.assertTrue(obj.test())


if __name__ == "__main__":
    unittest.main()
