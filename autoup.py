# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
import logging
import argparse
import sys

logger = logging.getLogger("autobit.autoup")


def handle_deluge(args):
    """ Deluge will send 3 arguments to the script on a completion event.

    - info_hash
    - name
    - path

    :see: http://dev.deluge-torrent.org/wiki/Plugins/Execute
    :return:
    :rtype:
    """
    pass



def handle_rtorrent():
    pass


def handle_qbt():
    pass


def make_command_parser():
    parser = argparse.ArgumentParser(description="AutoBit's torrent client on complete handler script")
    subparsers = parser.add_subparsers(help="sub command help")

    deluge_parser = subparsers.add_parser("deluge", help="Deluge compatible handler")
    deluge_parser.add_argument("info_hash", type=str, help="torrent info hash in hex format")
    deluge_parser.add_argument("name", type=str, help="Torrent name")
    deluge_parser.add_argument("path", type=str, help="Torrent filesystem location")
    deluge_parser.set_defaults(func=handle_deluge)

    rtorrent_parser = subparsers.add_parser("rtorrent", help="rTorrent compatible handler")
    rtorrent_parser.set_defaults(func=handle_rtorrent)

    qbt_parser = subparsers.add_parser("qbt", help="qBittorrent compatible handler")
    qbt_parser.set_defaults(func=handle_qbt)

    return parser

if __name__ == "__main__":
    try:
        args = make_command_parser().parse_args()
        args.func(args)
    except AttributeError:
        # No sub parser specified
        sys.exit(1)
