# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import

import unittest
from autobit import irc
from autobit import config
from autobit import db
from autobit.service.tl import TLParser
from autobit.service.ptp import PTPParser


class ParserTest(unittest.TestCase):
    def setUp(self):
        db.make_engine()

    def test_tl_parser(self):
        msg = "New Torrent Announcement: <Movies :: HD>  " \
              "Name:'Angles of Darkness 2015 480p WEBRiP SViD AC3-LEGi0N' " \
              "uploaded by 'GiGGLES' -  http://www.torrentleech.org/torrent/615195"
        tl_parser = TLParser()
        result = irc.process_line(tl_parser, msg)
        attr = result.guess()
        self.assertEqual({
            'screenSize': '480p',
            'type': 'movie',
            'title': 'angles of darkness',
            'audioCodec': 'AC3',
            'format': 'WEBRip',
            'releaseGroup': 'legi0n',
            'year': 2015}
            , attr
        )

    def test_ptp_parser(self):
        msg = "Mind's Eye AKA The Black Hole [2015] by Mark Steven Grove - x264 / WEB / MKV / 528x240 - " \
              "https://tls.passthepopcorn.me/torrents.php?id=128247&torrentid=363544 / " \
              "https://tls.passthepopcorn.me/torrents.php?action=download&id=363544 - sci.fi, thriller"
        tl_parser = PTPParser(config['ptp']['passkey'])
        result = parser.process_line(tl_parser, msg)
        attr = result.guess()
        self.assertEqual({
            'screenSize': '480p',
            'type': 'movie',
            'title': 'angles of darkness',
            'audioCodec': 'AC3',
            'format': 'WEBRip',
            'releaseGroup': 'legi0n',
            'year': 2015}
            , attr
        )


if __name__ == '__main__':
    unittest.main()
