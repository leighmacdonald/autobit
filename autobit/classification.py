# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
from enum import IntEnum, Enum
import guessit


class MediaType(IntEnum):
    """
    Defines the general type of media.
    """
    UNKNOWN = 0
    TV = 1
    MOVIE = 2

    @staticmethod
    def parse(media_type):
        if media_type in ["episode", "tv"]:
            return MediaType.TV
        elif media_type == "movie":
            return MediaType.MOVIE
        return MediaType.UNKNOWN


class ClassEnum(Enum):
    @classmethod
    def parse(cls, codec_name):
        try:
            return cls[codec_name.upper()]
        except KeyError:
            return cls.UNKNOWN


class Resolutions(ClassEnum):
    UNKNOWN = 0
    SD = 10
    P480 = 20
    P576 = 30
    P720 = 40
    I1080 = 50
    P1080 = 60
    K4 = 70


class Container(ClassEnum):
    UNKNOWN = 0
    MP4 = 1
    AVI = 2
    MKV = 3
    VOB = 4
    MPEG = 5
    ISO = 6
    WMV = 7
    TS = 8
    M4V = 9
    M2TS = 10


class Codecs(ClassEnum):
    """ Codecs detected in release"""
    UNKNOWN = 0
    XVID = 10
    X264 = 20
    MPEG2 = 30
    DIVX = 40
    DVDR = 50
    VC_1 = 60
    H264 = 70
    WMV = 80
    BD = 90
    X264_HI10P = 100


class Sources(ClassEnum):
    """ Media ripping sources """
    UNKNOWN = 0
    DSR = 1
    DVDRIP = 2
    TVRIP = 3
    VHSRIP = 4
    BLURAY = 5
    BDRIP = 6
    BRRIP = 7
    DVD5 = 8
    DVD9 = 9
    HDDVD = 10
    WEB_DL = 11
    WEBRIP = 12
    BD5 = 13
    BD9 = 14
    BD25 = 15

SOURCES_RETAIL = [Sources.DVDRIP, Sources.BLURAY, Sources.BDRIP, Sources.BRRIP, Sources.DVD5,
                  Sources.DVD9, Sources.HDDVD, Sources.BD5, Sources.BD9, Sources.BD25]


class Origin(ClassEnum):
    """
    Defines the origin of the release.
    """
    UNKNOWN = 0
    SCENE = 1
    P2P = 2

    # Special case for stopping spread of internal releases if wanted
    P2P_INTERNAL = 3

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
        name = ".".join(self.name.lower().split(" "))
        if self.type == MediaType.MOVIE:
            return self._key_sep.join([name, self.resolution])
        else:
            return self._key_sep.join([name, self.season, self.episode, self.resolution])

    @classmethod
    def from_guessit(cls, attrs):
        """ Use our own keys for the classifications via guessit

        :param attrs:
        :type attrs:
        :return: Parsed classification data
        :rtype: Classification
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
            try:
                if guessit_property == "type":
                    value = MediaType.parse(attrs.get(guessit_property, None))
                elif local_property == "codec_video":
                    value = Codecs.parse(attrs.get(guessit_property, None))

                else:
                    value = attrs.get(guessit_property, None)
            except ValueError:
                continue
            else:
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
        guess = Classification.from_guessit(attrs)
    except ValueError:
        return False
    else:
        return guess
