# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
import re
from autobit import config
from autobit.tracker import Tracker
from autobit.classification import MediaType


class PirateTheNet(Tracker):
    name = "ptn"
    rx = re.compile(r"^New in\s+(?P<section>.+?):\s(?P<name>.+?)\swith\s+\d+.+?\?id=(?P<id>\d+)$")

    def __init__(self):
        self._passkey = ""
        super().__init__()

    def parse_line(self, message: str):
        m = self.rx.match(message)
        if m:
            g = m.groupdict()
            release = self.make_release(g['name'], g['id'], MediaType.MOVIE)
            return release
        return None

    def download(self, release) -> bytes:
        url = "https://piratethenet.org/download.php?torrent={}&passkey={}".format(
            release.torrent_id, self._passkey
        )
        return self._fetch(url, verify=False)

    def reconfigure(self):
        self._passkey = config.get('PTN_PASSKEY', "")
        if self._passkey and len(self._passkey) == 32:
            self.enable()
        else:
            self.disable()

    def upload(self, release_name, torrent_file) -> bool:
        raise NotImplementedError()
