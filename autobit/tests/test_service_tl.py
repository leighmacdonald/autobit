# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import

import unittest

from autobit.service import tl
from autobit import db
from classification import MediaClass, MediaType


class TLParserTest(unittest.TestCase):
    def setUp(self):
        db.make_engine()

    def test_tl_parser(self):
        msg = "New Torrent Announcement: <Movies :: HD>  " \
              "Name:'Angles of Darkness 2015 480p WEBRiP SViD AC3-LEGi0N' " \
              "uploaded by 'GiGGLES' -  http://www.torrentleech.org/torrent/615195"

        result = tl.TLParser().parse_line(msg)
        self.assertEqual(MediaClass.MOVIE_HD, result.media_class)
        self.assertEqual(MediaType.MOVIE, result.media_type)
        self.assertEqual(615195, result.torrent_id)
        self.assertEqual("angles.of.darkness.2015.480p.webrip.svid.ac3-legi0n", result.name)


if __name__ == '__main__':
    unittest.main()
