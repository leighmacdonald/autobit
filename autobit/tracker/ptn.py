# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
from autobit import config
from autobit.tracker import Tracker
from autobit.db import Release


class PirateTheNet(Tracker):
    def __init__(self):
        self._passkey = ""
        super().__init__()

    def parse_line(self, message: str) -> Release:
        raise NotImplementedError()

    def download(self, release: Release) -> bytes:
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
