# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
from autobit import config
from autobit.tracker import Tracker
from autobit.db import Release


class BroadcastTheNet(Tracker):
    def __init__(self):
        self._authkey = ""
        self._passkey = ""
        super().__init__()

    def parse_line(self, message: str) -> Release:
        raise NotImplementedError()

    def download(self, release: Release) -> bytes:
        url = "https://broadcasthe.net/torrents.php?action=download&id={}&authkey={}&torrent_pass={}".format(
            release.torrent_id, self._authkey, self._passkey
        )
        return self._fetch(url)

    def reconfigure(self):
        self._authkey = config['BTN_AUTHKEY']
        self._passkey = config['BTN_PASSKEY']
        if all([self._authkey, self._passkey, len(self._authkey) == 32, len(self._passkey) == 32]):
            self.enable()
        else:
            self.disable()

    def upload(self, release_name, torrent_file) -> bool:
        raise NotImplementedError()
