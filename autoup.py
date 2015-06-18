# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
import logging
import sys

logger = logging.getLogger("autobit.autoup")

def handle_deluge():
    try:
        info_hash, name, path = sys.argv[0:3]
    except IndexError:
        logger.error("Not enough params")



def handle_rtorrent():
    pass


def handle_qbt():
    pass


if __name__ == "__main__":
    if "-r" in sys.argv:
        handle_rtorrent()
    elif "-q" in sys.argv:
        handle_qbt()
    else:
        handle_deluge()
