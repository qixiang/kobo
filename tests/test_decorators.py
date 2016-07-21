#!/usr/bin/python
# -*- coding: utf-8 -*-


import unittest

import tempfile
import os
import sys

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # noqa
sys.path.insert(0, PROJECT_DIR)  # noqa

from kobo.decorators import log_traceback

from common import read


class TestDecoratorsModule(unittest.TestCase):
    def setUp(self):
        self.tmp_file = tempfile.mktemp()

    def tearDown(self):
        os.remove(self.tmp_file)

    def test_log_traceback(self):
        @log_traceback(self.tmp_file)
        def foo_function():
            raise IOError("Some error")

        try:
            foo_function()
        except IOError:
            pass

        tb = read(self.tmp_file)
        self.assertTrue(tb.startswith("--- TRACEBACK BEGIN:"))


if __name__ == "__main__":
    unittest.main()
