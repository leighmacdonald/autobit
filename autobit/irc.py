# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
import abc
from guessit import guess_file_info
from autobit.db import Release
from autobit import db


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
    def parse_release_name(self, media_class: int, release_name: str) -> Release:
        pass

    @abc.abstractmethod
    def parse_line(self, message: str) -> Release:
        pass

    @abc.abstractmethod
    def verify_source(self, channel: str, nick: str) -> bool:
        pass


def parse_release_name(release_name: str) -> Release:
    guess = guess_file_info(release_name)


def process_line(parser: IRCParser, msg: str) -> Release:
    release = parser.parse_line(msg)
    if release:
        session = db.Session()
        if db.add_release(session, release):
            return release

    return False
