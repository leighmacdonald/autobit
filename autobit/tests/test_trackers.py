# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
import unittest
from autobit import db
from autobit.db import Release
from autobit.classification import MediaType
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
                   "http://www.torrentleech.org/torrent/615195"],
            'totv': [
                "[ Olympus - S01E10 -  Heritage ] [MP4 / x264 / HDTV / 480p / P2P] "
                "[ Olympus.S01E10.480p.HDTV.x264-mSD ] [ Syfy ] [ By: anonymous ] "
                "[ https://titansof.tv/api/torrents/17862/download ]"],
            'scc': [
                "NEW in TV/HD-x264: -> Republic.Of.Doyle.S01E02.720p.HDTV.x264-aAF "
                "(Uploaded 2 minutes and 6 seconds after pre) - (1.13 GB) - "
                "(https://sceneaccess.eu/details.php?id=1132683)"
            ],
            'btn': [
                "Game of Thrones | S05E08 | Episode | 2015 | MKV | h.264 | WEB-DL | 720p "
                "| No | Yes | 520543 | CloeJade | English "
                "| Game.of.Thrones.S05E08.Hardhome.720p.WEB-DL.DD5.1.H.264-NTb"
            ]
        }
        self.downloads = {
            'tl': [
                [Release("Angles of Darkness 2015 480p WEBRiP SViD AC3-LEGi0N", 615195,
                         MediaType.MOVIE, self.trackers['tl']), True]
            ],
            'totv': [
                [Release("Orange.Is.the.New.Black.S03E12.PROPER.720p.WEBRip.x264-2HD", 17856,
                         MediaType.TV, self.trackers['totv']), True]
            ],
            'btn': [
                [Release("StarTalk.S01E07.Chris.Hadfield.REAL.HDTV.x264-SQUEAK", 514266,
                         MediaType.TV, self.trackers['btn']), True]
            ],
            'ptp': [
                [Release("We Are Still Here 2015", 364285, MediaType.MOVIE, self.trackers['ptp']), True]
            ],

            'scc': [
                [Release("MasterChef.Australia.S07E29.PDTV.x264-FQM", 1134473,
                         MediaType.TV, self.trackers['scc']), True]
            ],
            'ptn': [
                [Release("Hannie.Caulder.1971.1080p.BluRay.x264-aAF", 91308,
                         MediaType.MOVIE, self.trackers['ptn']), True]
            ]
        }
        db.make_engine()

    def test_parse_line(self):
        for key, tracker in self.trackers.items():
            try:
                for input_message in self.irc_inputs[key]:
                    release = tracker.parse_line(input_message)
                    self.assertTrue(release.torrent_id > 0)
            except KeyError:
                pass
            except Exception as err:
                self.fail(err)

    def test_download(self):
        for key, tracker in self.trackers.items():
            if not tracker.enabled:
                continue
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
