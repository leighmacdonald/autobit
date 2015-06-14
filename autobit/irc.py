# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
import abc
from autobit import db
from autobit.db import Release
from autobit.tracker import Tracker


class ParsedLineInfo(object):
    category = None
    release_name = None


class IRCParser(object):
    __metaclass__ = abc.ABCMeta

    name = "irc_parser"

    source_nick = ""
    source_chan = ""

    @abc.abstractmethod
    def parse_media_type(self, media_class: str) -> int:
        pass

    @abc.abstractmethod
    def parse_line(self, message: str) -> Release:
        pass

    def verify_source(self, channel: str, nick: str) -> bool:
        return self.source_chan == channel.lower() and self.source_nick == nick.lower()


def process_line(parser: Tracker, msg: str) -> Release:
    release = parser.parse_line(msg)
    if release:
        session = db.Session()
        if db.add_release(session, release):
            return release

    return False
