# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import

import unittest

from autobit import db
from autobit.classification import MediaClass, MediaType
from autobit.tracker import tl
from autobit.tracker import totv
from autobit.tracker import ptp
from autobit.tracker import btn
from autobit.tracker import ptn
from autobit.tracker import scc
from db import Release


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
            ]
        }
        db.make_engine()

    def test_download(self):
        for key, tracker in self.trackers.items():
            try:
                for release, expected in self.downloads[key]:
                    self.assertTrue(tracker.download(release))
            except KeyError:
                pass


if __name__ == '__main__':
    unittest.main()
