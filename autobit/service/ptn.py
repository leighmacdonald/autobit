# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
from uploader import Uploader


class PTNUploader(Uploader):
    def configure(self, config):
        pass

    def upload(self, release_name, torrent_file) -> bool:
        pass
