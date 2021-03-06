# -*- coding: utf-8 -*-
"""
A module for TOTV providing full support for all the tracker functionality that autobit
supports.
"""
from __future__ import unicode_literals, absolute_import
import requests
from autobit import config
from autobit.classification import MediaType
from autobit.tracker import Tracker


class TitansOfTV(Tracker):
    name = "totv"
    announce_url = 'http://tracker.titansof.tv:34000/{}/announce'
    upload_endpoint = 'http://titansof.tv/api/torrents/upload'

    def __init__(self):
        self._apikey = ""
        super().__init__()

    def reconfigure(self):
        self._apikey = config.get("TOTV_APIKEY", "")
        if self._apikey and len(self._apikey) == 40:
            self.enable()
        else:
            self.disable()

    def download(self, release) -> bytes:
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
        return requests.post(self.upload_endpoint, payload).ok

    def parse_media_type(self, media_class: str) -> int:
        return MediaType.TV

    def parse_line(self, message: str):
        p = message.replace(" ", "")[1:-1].split("][")
        release_name = p[2]
        torrent_id = p[5].split("/")[5]
        return self.make_release(release_name, torrent_id, MediaType.TV)
