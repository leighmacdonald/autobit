# -*- coding: utf-8 -*-
"""
New Torrent Announcement: <Movies :: BDRip>  Name:'Angles of Darkness 2015 480p WEBRiP SViD AC3-LEGi0N' uploaded by 'GiGGLES' -  http://www.torrentleech.org/torrent/615195

http://www.torrentleech.org/download/615195/Angles.of.Darkness.2015.480p.WEBRiP.SViD.AC3-LEGi0N.torrent?
"""
from __future__ import unicode_literals, absolute_import
import logging
import re
from autobit import config
from autobit.classification import MediaClass
from autobit.tracker import Tracker
from autobit.db import Release
from classification import MediaType, TV_CLASSES

logger = logging.getLogger()


class TorrentLeech(Tracker):

    name = "tl"

    rx = re.compile(r"^New.+?<(?P<cat>.+?)>\s+Name:'(?P<name>.+?)'.+?/torrent/(?P<id>\d+)$")

    def __init__(self):
        self._apikey = None
        super().__init__()

    def parse_line(self, message: str) -> Release:
        m = self.rx.match(message)
        if m:
            g = m.groupdict()
            media_class = self.parse_media_type(g['cat'])
            if media_class == MediaClass.UNSUPPORTED:
                return None
            torrent_id = g.get('id', None)
            if not torrent_id:
                logging.warning("No torrent id found")
                return None
            media_type = self._get_media_type(media_class)
            return Release(g['name'], torrent_id, media_type, media_class, self.name)
        return None

    def _get_media_type(self, media_class):
        if media_class in [MediaClass.MOVIE_HD, MediaClass.MOVIE_SD]:
            return MediaType.MOVIE
        elif media_class in TV_CLASSES:
            return MediaType.EPISODE
        else:
            return MediaType.UNKNOWN

    def parse_media_type(self, media_class):
        if media_class == "Movies :: HD":
            return MediaClass.MOVIE_HD
        elif media_class == "Movies :: SD":
            return MediaClass.MOVIE_SD
        return MediaClass.UNSUPPORTED

    def download(self, release: Release) -> bytes:
        url = "http://www.torrentleech.org/rss/download/{}/{}/{}.torrent".format(
            release.torrent_id, self._apikey, release.name_orig.replace(" ", "."))
        torrent_data = self._fetch(url)
        return torrent_data

    def reconfigure(self):
        self._source_chan = config['TL_SOURCE_CHAN'].lower()
        self._source_nick = config['TL_SOURCE_NICK'].lower()
        self._apikey = config['TL_APIKEY']
        if self._apikey and len(self._apikey) == 20:
            self.enable()
        else:
            self.disable()

    def upload(self, release_name, torrent_file) -> bool:
        raise NotImplementedError()
