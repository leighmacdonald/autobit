# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
import re
from autobit import config
from autobit.tracker import Tracker
from autobit.db import Release
from autobit.classification import MediaType

section_map = {
    "TV/SD-X264": [MediaType.TV],
    "TV/HD-X264": [MediaType.TV],
    "Foreign/TV/x264": [MediaType.TV],
    "Movies/x264": [MediaType.MOVIE],
    "Movies/XviD": [MediaType.MOVIE],
    "Foreign/Movies/XviD": [MediaType.MOVIE],
    "Foreign/Movies/x264": [MediaType.MOVIE]
}

class SceneAccess(Tracker):
    """
    > (~SCC@bot.sceneaccess.org): SCC BOT
    > NEW in TV/HD-x264: -> Republic.Of.Doyle.S01E02.720p.HDTV.x264-aAF (Uploaded 2 minutes and 6 seconds after pre) - (1.13 GB) - (https://sceneaccess.eu/details.php?id=1132683)
    """

    def __init__(self):
        self._rx = re.compile(r".+?in\s+(?P<section>.+?):.+>\s+(?P<rls>.+?)\s+.+=(?P<id>\d+)\)$")
        self._passkey = ""
        self.name = "scc"
        super().__init__()

    def parse_line(self, message: str) -> Release:
        match = self._rx.match(message)
        if match:
            g = match.groupdict()
            torrent_id = g['id']
            release_name = g['rls']
            section = g['section']
            return self.make_release(release_name, torrent_id, MediaType.TV)

    def download(self, release: Release) -> bytes:
        url = "https://sceneaccess.eu/download/{}/{}/{}.torrent".format(
            release.torrent_id, self._passkey, release.name_orig)
        torrent_file = self._fetch(url)
        return torrent_file

    def reconfigure(self):
        self._passkey = config["SCC_PASSKEY"]
        if self._passkey and len(self._passkey) == 32:
            self.enable()
        else:
            self.disable()

    def upload(self, release_name, torrent_file) -> bool:
        raise NotImplementedError()
