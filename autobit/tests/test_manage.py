# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
import tempfile
import unittest
from os.path import join, exists
from autobit import manage, config
from autobit.db import Release
from autobit.tracker import totv
from autobit.classification import MediaType, MediaClass


class TestManage(unittest.TestCase):

    def test_write_to_watch(self):
        fname = "test_file.torrent"
        torrent_data = b"torrent_file_data"
        watch_dir = tempfile.mkdtemp()
        config["WATCH_DIR"] = watch_dir
        manage.write_to_watch(torrent_data, fname)
        out_file = join(watch_dir, fname)
        self.assertTrue(exists(out_file))
        self.assertEqual(torrent_data, open(out_file, "rb").read())

    def test_process_release(self):
        tkr = totv.TitansOfTV()
        release = Release("Orange.Is.the.New.Black.S03E12.PROPER.720p.WEBRip.x264-2HD", 17856,
                          MediaType.EPISODE, MediaClass.TV_HD, 'totv')
        manage.process_release(tkr, release)


if __name__ == '__main__':
    unittest.main()
