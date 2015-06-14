# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import

import unittest

from autobit import db
from autobit.db import Release
from autobit.classification import MediaClass, MediaType
from autobit.tracker import tl
from autobit.tracker import totv
from autobit.tracker import ptp
from autobit.tracker import btn
from autobit.tracker import ptn
from autobit.tracker import scc


class TrackerTest(unittest.TestCase):
    def setUp(self):
        self.trackers = {
            'tl': tl.TorrentLeech(),
            'totv': totv.TitansOfTV(),
            'ptp': ptp.PassThePopcorn(),
            'scc': scc.SceneAccess(),
            'ptn': ptn.PirateTheNet(),
            'btn': btn.BroadcastTheNet()
        }
        self.irc_inputs = {
            'tl': ["New Torrent Announcement: <Movies :: HD>  Name:'Angles of Darkness 2015 "
                   "480p WEBRiP SViD AC3-LEGi0N' uploaded by 'GiGGLES' -  "
                   "http://www.torrentleech.org/torrent/615195"]
        }
        self.downloads = {
            'tl': [
                [Release("Angles of Darkness 2015 480p WEBRiP SViD AC3-LEGi0N", 615195,
                         MediaType.MOVIE, MediaClass.MOVIE_SD, 'tl'), True]
            ],
            'totv': [
                [Release("Orange.Is.the.New.Black.S03E12.PROPER.720p.WEBRip.x264-2HD", 17856,
                         MediaType.EPISODE, MediaClass.TV_HD, 'totv'), True]
            ],
            'btn': [
                [Release("StarTalk.S01E07.Chris.Hadfield.REAL.HDTV.x264-SQUEAK", 514266,
                         MediaType.EPISODE, MediaClass.TV_HD, 'btn'), True]
            ],
            'ptp': [
                [Release("We Are Still Here 2015", 364285, MediaType.MOVIE, MediaClass.MOVIE_HD, 'ptp'), True]
            ],

            'scc': [
                [Release("MasterChef.Australia.S07E29.PDTV.x264-FQM", 1134473,
                         MediaType.EPISODE, MediaClass.TV_SD, 'scc'), True]
            ],
            'ptn': [
                [Release("Hannie.Caulder.1971.1080p.BluRay.x264-aAF", 91308,
                         MediaType.MOVIE, MediaClass.MOVIE_HD, "ptn"), True]
            ]
        }
        db.make_engine()

    def test_download(self):
        for key, tracker in self.trackers.items():
            try:
                for release, expected in self.downloads[key]:
                    torrent_file = tracker.download(release)
                    self.assertTrue(torrent_file.startswith(b"d8:announce"))
            except KeyError:
                pass
            except Exception as err:
                self.fail(err)


if __name__ == '__main__':
    unittest.main()
