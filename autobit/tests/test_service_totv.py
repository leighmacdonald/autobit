# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import

import unittest

from autobit.service import totv
from autobit import db
from classification import MediaClass, MediaType


class TOTVParserTest(unittest.TestCase):
    def setUp(self):
        db.make_engine()

    def test_totv_parser(self):
        msg = "[ Orange Is the New Black - S03E01 - It's the Great Blumpkin, Charlie Brown ] [MKV / x264 / WEBRip / 720p / P2P] [ Orange.Is.The.New.Black.S03E01.Mothers.Day.720p.NF.WEBRip.DD5.1.x264-NTb ] [ Netflix ] [ By: anonymous ] [ https://titansof.tv/api/torrents/17696/download ]"

        result = totv.TOTVParser().parse_line(msg)
        self.assertEqual(MediaClass.MOVIE_HD, result.media_class)
        self.assertEqual(MediaType.MOVIE, result.media_type)
        self.assertEqual(615195, result.torrent_id)
        self.assertEqual("angles.of.darkness.2015.480p.webrip.svid.ac3-legi0n", result.name)


if __name__ == '__main__':
    unittest.main()
