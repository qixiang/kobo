#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import sys
import unittest
import logging

import six

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # noqa
sys.path.insert(0, PROJECT_DIR)  # noqa

import kobo.log  # noqa


class TestLog(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger("TestLogger")

    def test_verbose_hack(self):
        self.logger.verbose("foo")
        logging.verbose("foo")
        self.assertEqual(logging.VERBOSE, 15)
        if six.PY2:
            self.assertIn("VERBOSE", logging._levelNames)
            self.assertEqual(logging._levelNames[15], "VERBOSE")
        else:
            self.assertEqual(logging._nameToLevel["VERBOSE"], 15)


if __name__ == '__main__':
    unittest.main()
