# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
from autobit import config
from autobit.tracker import Tracker
from autobit.db import Release


class SceneAccess(Tracker):
    """
    > (~SCC@bot.sceneaccess.org): SCC BOT
    > NEW in TV/HD-x264: -> Republic.Of.Doyle.S01E02.720p.HDTV.x264-aAF (Uploaded 2 minutes and 6 seconds after pre) - (1.13 GB) - (https://sceneaccess.eu/details.php?id=1132683)
    """

    def __init__(self):
        self._passkey = ""
        super().__init__()

    def parse_line(self, message: str) -> Release:
        raise NotImplementedError()

    def download(self, release: Release) -> bytes:
        url = "https://sceneaccess.eu/download/{}/{}/{}.torrent".format(
            release.torrent_id, self._passkey, release.name_orig)
        torrent_file = self._fetch(url)
        return torrent_file

    def reconfigure(self):
        self._passkey = config["SCC_PASSKEY"]

    def upload(self, release_name, torrent_file) -> bool:
        raise NotImplementedError()
