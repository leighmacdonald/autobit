# -*- coding: utf-8 -*-
"""
New Torrent Announcement: <Movies :: BDRip>  Name:'Angles of Darkness 2015 480p WEBRiP SViD AC3-LEGi0N' uploaded by 'GiGGLES' -  http://www.torrentleech.org/torrent/615195

http://www.torrentleech.org/download/615195/Angles.of.Darkness.2015.480p.WEBRiP.SViD.AC3-LEGi0N.torrent?
"""
from __future__ import unicode_literals, absolute_import
import re
from autobit.parser import IRCParser, MediaClass
from autobit.db import Release


class TLParser(IRCParser):
    name = "tl"
    source_nick = "_AnnounceBot_".lower()
    source_chan = "#tlannounces".lower()

    rx = re.compile(r"^New.+?<(?P<cat>.+?)>\s+Name:'(?P<name>.+?)'.+?/torrent/(?P<id>\d+)$")

    def parse_line(self, message: str) -> Release:
        m = self.rx.match(message)
        if m:
            g = m.groupdict()
            media_type = self.parse_media_type(g['cat'])
            if media_type == MediaClass.UNSUPPORTED:
                return None
            release = Release(g['name'], media_type, self.name)
            return release
        return None

    def parse_media_type(self, media_class):
        if media_class == "Movies :: HD":
            return MediaClass.MOVIE_HD
        elif media_class == "Movies :: SD":
            return MediaClass.MOVIE_SD
        return MediaClass.UNSUPPORTED

    def parse_release_name(self, media_class: MediaClass, release_name: str) -> Release:
        pass

    def verify_source(self, channel: str, nick: str) -> bool:
        return self.source_chan == channel.lower() and self.source_nick == nick.lower()


