# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
from enum import IntEnum
import guessit


class Classification(object):
    """
    Provides classification info for a parsed release name
    """

    _key_sep = "-"

    def __init__(self):
        self.name = ""
        self.episode = None
        self.format = None
        self.resolution = None
        self.codec_video = None
        self.codec_audio = None
        self.season = None
        self.type = None
        self.year = None
        self.group = None

    @property
    def key(self):
        """ Generates and returns a key that uniquely defines the release
        in a uniform/normalized manner so that its simple to search for previous
        matching keys.

        :return: Generated release key
        :rtype: str
        """
        if self.type == MediaType.MOVIE:
            return self._key_sep.join([self.name.lower(), self.resolution])
        else:
            return self._key_sep.join([self.name.lower(), self.season, self.episode, self.resolution])

    @classmethod
    def from_guessit(cls, attrs):
        """ Use our own keys for the classifications via guessit

        :param attrs:
        :type attrs:
        :return:
        :rtype:
        """
        c = cls()
        attr_list = [
            ["season", "season"],
            ["type", "type"],
            ["episode", "episodeNumber"],
            ["format", "format"],
            ["group", "releaseGroup"],
            ["resolution", "screenSize"],
            ["codec_video", "videoCodec"],
            ["year", "year"]
        ]
        for local_property, guessit_property in attr_list:
            if guessit_property == "type":
                value = MediaType.parse(attrs.get("type", None))
            else:
                value = attrs.get(guessit_property, None)
            setattr(c, local_property, value)

        if c.type == MediaType.MOVIE:
            setattr(c, "name", attrs.get("title", None))
        else:
            setattr(c, "name", attrs.get("series", None))

        if not c.name or not c.type:
            raise ValueError("Incomplete classification")

        if c.type == MediaType.MOVIE and c.format in ["HDTV"]:
            raise ValueError("Incompatible match values")

        return c


class MediaClass(IntEnum):
    UNSUPPORTED = 0
    TV_SD = 1
    TV_HD = 2
    MOVIE_SD = 3
    MOVIE_HD = 4


class MediaType(IntEnum):
    UNKNOWN = 0
    EPISODE = 1
    MOVIE = 2

    @staticmethod
    def parse(media_type):
        if media_type == "episode":
            return MediaType.EPISODE
        elif media_type == "movie":
            return MediaType.MOVIE
        return MediaType.UNKNOWN


def classify(release_name, section_hint=None):
    """

    :param release_name:
    :param section_hint:
    :return: Parsed classification data|bool
    :rtype: Classification
    """
    if section_hint not in ["video", "movie", "episode", None, False, ""]:
        raise ValueError("Invalid section hint type")
    attrs = guessit.guess_file_info(release_name.lower(), options={'name_only': True}, type=section_hint)
    try:
        for k in ['releaseGroup', 'format', 'type']:
            # Reject anything we cant be sure of to be safe
            if k not in attrs:
                raise ValueError()
        return Classification.from_guessit(attrs)
    except ValueError:
        return False
