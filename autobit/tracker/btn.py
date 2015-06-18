# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
from autobit import config
from autobit import ConfigError
from autobit.tracker import Tracker
from autobit.classification import MediaType


class BroadcastTheNet(Tracker):
    def __init__(self):
        self.name = "btn"
        self._authkey = ""
        self._passkey = ""
        super().__init__()

    def parse_line(self, message: str):
        pcs = message.split(" | ")
        rls_name = pcs[-1]
        torrent_id = pcs[10]
        return self.make_release(rls_name, torrent_id, MediaType.TV)

    def download(self, release) -> bytes:
        url = "https://broadcasthe.net/torrents.php?action=download&id={}&authkey={}&torrent_pass={}".format(
            release.torrent_id, self._authkey, self._passkey
        )
        return self._fetch(url)

    def reconfigure(self):
        try:
            self._authkey = config['BTN_AUTHKEY']
            self._passkey = config['BTN_PASSKEY']
            if all([self._authkey, self._passkey, len(self._authkey) == 32, len(self._passkey) == 32]):
                raise ConfigError()
        except (KeyError, ConfigError):
            self.disable()
        else:
            self.enable()

    def upload(self, release_name, torrent_file) -> bool:
        raise NotImplementedError()
