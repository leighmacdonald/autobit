# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
from autobit import db
from autobit import tracker
from autobit import TrackerError, AutoBitError


def process_release(tkr: tracker.Tracker, release: db.Release):
    try:
        torrent_file = tkr.download(release)
        if not torrent_file:
            raise TrackerError("Downloaded torrent file invalid")
    except TrackerError as err:
        pass
    except AutoBitError as err:
        pass
    except Exception as err:
        pass
    else:
        pass
