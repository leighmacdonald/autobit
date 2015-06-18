# -*- coding: utf-8 -*-
"""
<Hummingbird> I pirati della costa AKA Pirates of the Coast [1960] by Domenico Paolella - x264 / DVD / MKV / 720x302 - https://tls.passthepopcorn.me/torrents.php?id=128243&torrentid=363540 / https://tls.passthepopcorn.me/torrents.php?action=download&id=363540 - adventure
"""
from __future__ import unicode_literals, absolute_import
import re
from autobit import config
from autobit.tracker import Tracker
from autobit.classification import MediaType


class PassThePopcorn(Tracker):
    name = "ptp"
    rx = re.compile(r"^(?P<name>.+?)\s-\shttps://.+?torrentid=(?P<id>\d+)")

    def __init__(self):
        self._passkey = ""
        self._authkey = ""
        super().__init__()

    def reconfigure(self):
        self._passkey = config.get('PTP_PASSKEY', "")
        self._authkey = config.get('PTP_AUTHKEY', "")
        if self._passkey and self._authkey and len(self._passkey) == 32 and self._authkey > 0:
            self.enable()
        else:
            self.disable()

    def parse_line(self, message: str):
        m = self.rx.match(message)
        if m:
            g = m.groupdict()
            release = self.make_release(g['name'], g['id'], MediaType.MOVIE)
            return release
        return None

    def upload(self, release_name, torrent_file) -> bool:
        pass

    def download(self, release) -> bytes:
        url = "http://passthepopcorn.me/torrents.php?action=download&torrent_pass={}&id={}&authkey={}".format(
            self._passkey, release.torrent_id, self._authkey
        )
        torrent_file = self._fetch(url)
        return torrent_file
