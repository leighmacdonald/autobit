# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
import requests
from autobit import config
from autobit.classification import MediaType
from autobit.db import Release
from autobit.tracker import Tracker


class TitansOfTV(Tracker):
    announce_url = 'http://tracker.titansof.tv:34000/{}/announce'
    upload_endpoint = 'http://titansof.tv/api/torrents/upload'

    def __init__(self):
        self._apikey = ""
        super().__init__()

    def reconfigure(self):
        self._apikey = config["TOTV_APIKEY"]

    def download(self, release: Release) -> bytes:
        url = "https://titansof.tv/api/torrents/{}/download".format(release.torrent_id)
        torrent_file = self._fetch(url, params={"apikey": self._apikey})
        return torrent_file

    def upload(self, release_name, torrent_file) -> bool:
        payload = {
            'torrent_file': torrent_file,
            'release_name': release_name.replace(' ', '.').replace('_', '.'),
            'anonymous': 1,
            'scene_numbering': 1
        }
        requests.post(self.upload_endpoint, payload)

    def parse_media_type(self, media_class: str) -> int:
        return MediaType.EPISODE

    def parse_release_name(self, media_class: int, release_name: str) -> Release:
        pass

    def parse_line(self, message: str) -> Release:
        pass
