# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
import requests
from autobit.uploader import Uploader


class ToTVUploader(Uploader):
    announce_url = 'http://tracker.titansof.tv:34000/{}/announce'
    upload_endpoint = 'http://titansof.tv/api/torrents/upload'

    def configure(self, config):
        pass

    def upload(self, release_name, torrent_file) -> bool:
        payload = {
            'torrent_file': torrent_file,
            'release_name': release_name.replace(' ', '.').replace('_', '.'),
            'anonymous': 1,
            'scene_numbering': 1
        }
        requests.post(self.upload_endpoint, payload)
