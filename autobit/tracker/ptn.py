# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
from autobit.tracker import Tracker
from autobit.db import Release


class PirateTheNet(Tracker):
    def parse_line(self, message: str) -> Release:
        raise NotImplementedError()

    def download(self, release: Release) -> bytes:
        raise NotImplementedError()

    def reconfigure(self):
        pass

    def upload(self, release_name, torrent_file) -> bool:
        raise NotImplementedError()
