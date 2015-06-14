# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
from autobit.tracker import Tracker
from autobit.db import Release


class SceneAccess(Tracker):
    """
    > (~SCC@bot.sceneaccess.org): SCC BOT
    > NEW in TV/HD-x264: -> Republic.Of.Doyle.S01E02.720p.HDTV.x264-aAF (Uploaded 2 minutes and 6 seconds after pre) - (1.13 GB) - (https://sceneaccess.eu/details.php?id=1132683)
    """

    def parse_line(self, message: str) -> Release:
        raise NotImplementedError()

    def download(self, release: Release) -> bytes:
        raise NotImplementedError()

    def reconfigure(self):
        pass

    def upload(self, release_name, torrent_file) -> bool:
        raise NotImplementedError()
