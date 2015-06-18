# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
import logging
from os.path import join
from autobit import db
from autobit import tracker
from autobit import TrackerError, AutoBitError
from autobit import config

logger = logging.getLogger()


def write_to_watch(torrent_file: bytes, file_name: str):
    with open(join(config["WATCH_DIR"], file_name), "wb") as tf:
        tf.write(torrent_file)
        logger.info("Added torrent file to watch: {}".format(file_name))


def process_release(release: db.Release):
    session = db.Session()
    try:
        torrent_file = release.download()
        if not torrent_file:
            raise TrackerError("Downloaded torrent file invalid")
        file_name = "{}.torrent".format(release.name)
        write_to_watch(torrent_file, file_name=file_name)

    except TrackerError as err:
        pass
    except AutoBitError as err:
        pass
    except Exception as err:
        pass
