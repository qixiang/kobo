#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import sys
import tempfile
import unittest

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # noqa
sys.path.insert(0, PROJECT_DIR)  # noqa

from kobo.http import POSTTransport


class TestPOSTTransport(unittest.TestCase):

    def setUp(self):
        self.postt = POSTTransport()
        self.temp_files = []

    def tearDown(self):
        for i in self.temp_files:
            try:
                os.unlink(i)
            except:
                pass

    def _create_temp_file(self, *args, **kwargs):
        temp_file = tempfile.mkstemp(*args, **kwargs)[1]
        self.temp_files.append(temp_file)
        return temp_file

    def test_get_content_type(self):
        tf0 = self._create_temp_file()
        tf1 = self._create_temp_file(suffix=".txt")
        tf2 = self._create_temp_file(suffix=".rtf")
        tf3 = self._create_temp_file(suffix=".avi")

        self.assertEqual(self.postt.get_content_type(tf0), "application/octet-stream")
        self.assertEqual(self.postt.get_content_type(tf1), "text/plain")
        # *.rtf: py2.7 returns 'application/rtf'; py2.4 returns 'text/rtf'
        self.assertEqual(self.postt.get_content_type(tf2).split("/")[1], "rtf")
        self.assertIn(self.postt.get_content_type(tf2), ["application/rtf", "text/rtf"])
        self.assertEqual(self.postt.get_content_type(tf3), "video/x-msvideo")

    def test_add_file(self):
        tf1 = self._create_temp_file()
        tf2 = self._create_temp_file()
        tf3 = self._create_temp_file()

        # can't add file that doesn't exist
        os.unlink(tf1)
        self.assertRaises(OSError, self.postt.add_file, "file", tf1)

        # add existing file
        self.assertEqual(self.postt.add_file("file", tf2), None)

        # can't add a file object
        tf3_fo = open(tf3)
        self.assertRaises(TypeError, self.postt.add_file, "file", tf3_fo)
        tf3_fo.close()


if __name__ == '__main__':
    unittest.main()
