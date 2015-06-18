# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
from os import makedirs, unlink
import tempfile
import shutil
import unittest
from os.path import exists, join
from autobit import archive
from autobit.tests import fixture_root

class TestArchive(unittest.TestCase):
    rls_a = ""
    rls_b = ""
    archive_root = join(fixture_root, "archives")

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="autobit")
        self.rls_a_path = join(self.temp_dir, self.rls_a)
        self.rls_b_path = join(self.temp_dir, self.rls_b)
        for path in [self.rls_a_path, self.rls_b_path]:
            try:
                makedirs(path)
            except FileExistsError:
                pass

    def tearDown(self):
        if exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_extract_release(self):
        paths = ["long_naming", "standard_naming", "uncompressed"]
        for path in (join(self.archive_root, p) for p in paths):
            found_file = archive.find_rar(path)
            extracted_file = archive.extract_rar(found_file, self.temp_dir)
            self.assertTrue(exists(extracted_file))
            try:
                unlink(extracted_file)
            except OSError:
                pass



if __name__ == '__main__':
    unittest.main()
