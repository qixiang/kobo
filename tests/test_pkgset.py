#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import sys
import unittest
import tempfile
import shutil
import hashlib
import pickle as pickle

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # noqa
sys.path.insert(0, PROJECT_DIR)  # noqa

import six

from kobo.pkgset import FileWrapper, RpmWrapper, SimpleRpmWrapper, FileCache

from common import read, write


class TestFileWrapperClass(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.file_path = os.path.join(self.tmp_dir, "file")

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_file_name_property(self):
        write(self.file_path, "hello\n")
        wrap = FileWrapper(self.file_path)
        self.assertEqual(wrap.file_path, self.file_path)
        self.assertEqual(wrap.file_name, os.path.basename(self.file_path))

    def test_compute_checksums(self):
        write(self.file_path, "hello\n")

        res_origin = {}
        for name in ("md5", "sha1", "sha256", "sha512"):
            m = hashlib.new(name)
            data = read(self.file_path)
            m.update(six.b(data))
            res_origin[name] = m.hexdigest()

        wrap = FileWrapper(self.file_path)
        res = wrap.compute_checksums(["md5", "sha1", "sha256", "sha512"])
        self.assertEqual(res_origin, res)

    def test_pickle(self):
        self.test_file_name_property()
        name = "file"
        file1 = os.path.join(self.tmp_dir, name)
        wrap = FileWrapper(file1)
        pickled_data = pickle.dumps(wrap)
        wrap2 = pickle.loads(pickled_data)
        self.assertEqual(wrap.file_path, wrap2.file_path)


class TestRpmWrapperClass(unittest.TestCase):
    def setUp(self):
        self.file_path = "data/dummy-basesystem-10.0-6.noarch.rpm"
        self.source_path = "data/dummy-basesystem-10.0-6.src.rpm"
        self.nosource_path = "data/dummy-AdobeReader_enu-9.5.1-1.nosrc.rpm"

    def test_is_source(self):
        wrap = RpmWrapper(self.file_path)
        self.assertEqual(wrap.sourcepackage, None)
        self.assertEqual(wrap.is_source, False)
        self.assertEqual(wrap.nosource, [])
        wrap = RpmWrapper(self.source_path)
        self.assertEqual(wrap.sourcepackage, True)
        self.assertEqual(wrap.is_source, True)
        self.assertEqual(wrap.nosource, [])
        wrap = RpmWrapper(self.nosource_path)
        self.assertEqual(wrap.sourcepackage, True)
        self.assertEqual(wrap.is_source, True)
        self.assertEqual(wrap.nosource, [0])

    def test_is_system_release(self):
        wrap = RpmWrapper(self.file_path)
        self.assertEqual(wrap.is_system_release, False)

    def test_pickle(self):
        wrap = RpmWrapper(self.file_path)
        pickled_data = pickle.dumps(wrap)
        wrap2 = pickle.loads(pickled_data)
        self.assertEqual(wrap.name, wrap2.name)


class TestSimpleRpmWrapperClass(unittest.TestCase):
    def setUp(self):
        self.file_path = "data/dummy-basesystem-10.0-6.noarch.rpm"
        self.source_path = "data/dummy-basesystem-10.0-6.src.rpm"

    def test_is_source(self):
        wrap = SimpleRpmWrapper(self.file_path)
        self.assertEqual(wrap.is_source, False)
        wrap = SimpleRpmWrapper(self.source_path)
        self.assertEqual(wrap.is_source, True)

    def test_is_system_release(self):
        wrap = RpmWrapper(self.file_path)
        self.assertEqual(wrap.is_system_release, False)

    def test_pickle(self):
        wrap = SimpleRpmWrapper(self.file_path)
        pickled_data = pickle.dumps(wrap)
        wrap2 = pickle.loads(pickled_data)
        self.assertEqual(wrap.name, wrap2.name)


class TestFileCacheClass(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.cache = FileCache()
        self.file1 = os.path.join(self.tmp_dir, "file_1")
        self.file2 = os.path.join(self.tmp_dir, "file_2")

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_add_two_same_hardlinks(self):
        write(self.file1, "hello\n")
        os.link(self.file1, self.file2)

        self.cache = FileCache()
        wrap1 = self.cache.add(self.file1)
        wrap2 = self.cache.add(self.file2)

        self.assertEqual(len(self.cache.inode_cache), 1)
        self.assertEqual(len(self.cache.file_cache), 1)
        self.assertEqual(len(self.cache), 1)
        self.assertEqual(id(wrap1), id(wrap2))

    def test_add_two_different_files(self):
        write(self.file1, "roses are red\n")
        write(self.file2, "violets are blue\n")

        self.cache = FileCache()
        wrap1 = self.cache.add(self.file1)
        wrap2 = self.cache.add(self.file2)

        self.assertEqual(len(self.cache.inode_cache), 2)
        self.assertEqual(len(self.cache.file_cache), 2)
        self.assertEqual(len(self.cache), 2)
        self.assertNotEqual(id(wrap1), id(wrap2))

    def test_getitem(self):
        write(self.file1, "hello\n")
        write(self.file2, "hello\n")

        self.cache = FileCache()
        wrap1 = self.cache.add(self.file1)
        wrap2 = self.cache.add(self.file2)

        self.assertEqual(len(self.cache.inode_cache), 2)
        self.assertEqual(len(self.cache.file_cache), 2)
        self.assertEqual(id(self.cache[self.file1]), id(wrap1))
        self.assertEqual(id(self.cache[self.file2]), id(wrap2))

    def test_setitem(self):
        write(self.file1, "hello\n")

        self.cache1 = FileCache()
        self.cache2 = FileCache()
        wrap = self.cache1.add(self.file1)

        self.cache2[self.file1] = wrap

        self.assertEqual(len(self.cache2.file_cache), 1)
        self.assertEqual(id(self.cache2[self.file1]), id(wrap))

    def test_iteritems(self):
        write(self.file1, "hello\n")
        write(self.file2, "hello\n")

        self.cache = FileCache()
        self.cache.add(self.file1)
        self.cache.add(self.file2)

        items = [path for path, _ in list(self.cache.items())]

        self.assertEqual(len(self.cache.inode_cache), 2)
        self.assertEqual(len(self.cache.file_cache), 2)
        self.assertEqual(len(items), 2)
        self.assertIn(self.file1, items)
        self.assertIn(self.file2, items)

    def test_iter(self):
        write(self.file1, "hello\n")
        write(self.file2, "hello\n")

        self.cache = FileCache()
        self.cache.add(self.file1)
        self.cache.add(self.file2)

        items = [item for item in self.cache]

        self.assertEqual(len(self.cache.inode_cache), 2)
        self.assertEqual(len(self.cache.file_cache), 2)
        self.assertEqual(len(items), 2)
        self.assertIn(self.file1, items)
        self.assertIn(self.file2, items)

    def test_remove_by_file_path(self):
        self.test_add_two_different_files()
        self.cache.remove(self.file1)

        items = [item for item in self.cache]

        self.assertEqual(len(self.cache.inode_cache), 1)
        self.assertEqual(len(self.cache.file_cache), 1)
        self.assertEqual(len(items), 1)
        self.assertNotIn(self.file1, items)
        self.assertIn(self.file2, items)

    def test_remove_by_obj(self):
        self.test_add_two_different_files()

        self.file1_obj = self.cache[self.file1]
        self.cache.remove(self.file1_obj)

        items = [item for item in self.cache]

        self.assertEqual(len(self.cache.inode_cache), 1)
        self.assertEqual(len(self.cache.file_cache), 1)
        self.assertEqual(len(items), 1)
        self.assertNotIn(self.file1, items)
        self.assertIn(self.file2, items)

    def test_remove_by_filenames(self):
        self.test_add_two_different_files()

        # add a file with existing name to a subdir
        os.makedirs(os.path.join(self.tmp_dir, "dir"))
        file1a = os.path.join(self.tmp_dir, "dir", "file_1")
        write(file1a, "hello\n")
        self.cache.add(file1a)

        self.cache.remove_by_filenames("does-not-exist")
        self.assertEqual(len(self.cache.inode_cache), 3)
        self.assertEqual(len(self.cache.file_cache), 3)

        # ignores the path, only the file name is important
        # removes both files with the file name "file_1"
        self.cache.remove_by_filenames("/foo/bar/file_1")

        items = [item for item in self.cache]

        self.assertEqual(len(self.cache.inode_cache), 1)
        self.assertEqual(len(self.cache.file_cache), 1)
        self.assertEqual(len(items), 1)
        self.assertNotIn(self.file1, items)
        self.assertIn(self.file2, items)


if __name__ == "__main__":
    unittest.main()
