# -*- coding: utf-8 -*-
"""
<Hummingbird> I pirati della costa AKA Pirates of the Coast [1960] by Domenico Paolella - x264 / DVD / MKV / 720x302 - https://tls.passthepopcorn.me/torrents.php?id=128243&torrentid=363540 / https://tls.passthepopcorn.me/torrents.php?action=download&id=363540 - adventure
"""
from __future__ import unicode_literals, absolute_import
import re
from autobit import config
from autobit.db import Release
from autobit.tracker import Tracker
from autobit.classification import MediaClass


class PassThePopcorn(Tracker):
    name = "ptp"
    rx = re.compile(r"^(?P<name>.+?)\s-\shttps://.+?torrentid=(?P<id>\d+)")

    def __init__(self):
        self._passkey = ""
        self._authkey = ""
        super().__init__()

    def reconfigure(self):
        self._passkey = config['PTP_PASSKEY']
        self._authkey = int(config.get('PTP_AUTHKEY', 0))
        if self._passkey and self._authkey and len(self._passkey) == 32 and self._authkey > 0:
            self.enable()
        else:
            self.disable()

    def parse_line(self, message: str) -> Release:
        m = self.rx.match(message)
        if m:
            g = m.groupdict()
            media_type = self.parse_media_type(g['cat'])
            if media_type == MediaClass.UNSUPPORTED:
                return None
            release = Release(g['name'], media_type, self.name)
            return release
        return None

    def parse_media_type(self, media_class):
        if media_class == "Movies :: HD":
            return MediaClass.MOVIE_HD
        elif media_class == "Movies :: SD":
            return MediaClass.MOVIE_SD
        return MediaClass.UNSUPPORTED

    def upload(self, release_name, torrent_file) -> bool:
        pass

    def download(self, release: Release) -> bytes:
        url = "http://passthepopcorn.me/torrents.php?action=download&torrent_pass={}&id={}&authkey={}".format(
            self._passkey, release.torrent_id, self._authkey
        )
        torrent_file = self._fetch(url)
        return torrent_file
