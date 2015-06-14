# -*- coding: utf-8 -*-
"""
<Hummingbird> I pirati della costa AKA Pirates of the Coast [1960] by Domenico Paolella - x264 / DVD / MKV / 720x302 - https://tls.passthepopcorn.me/torrents.php?id=128243&torrentid=363540 / https://tls.passthepopcorn.me/torrents.php?action=download&id=363540 - adventure
<Hummingbird> Dál nic AKA Byeway [2013] by Ivo Bystrican - x264 / WEB / MKV / 720p - https://tls.passthepopcorn.me/torrents.php?id=128244&torrentid=363541 / https://tls.passthepopcorn.me/torrents.php?action=download&id=363541 - documentary
<Hummingbird> Uno [2002] by Zsombor Dyga - x264 / DVD / AVI / 624x326 - https://tls.passthepopcorn.me/torrents.php?id=128245&torrentid=363542 / https://tls.passthepopcorn.me/torrents.php?action=download&id=363542 - action, drama, sci.fi, short
<Hummingbird> Una [1984] by Milos 'Misa' Radivojevic - x264 / DVD / MKV / 694x454 - https://tls.passthepopcorn.me/torrents.php?id=128246&torrentid=363543 / https://tls.passthepopcorn.me/torrents.php?action=download&id=363543 - drama, romance
<Hummingbird> Mind's Eye AKA The Black Hole [2015] by Mark Steven Grove - x264 / WEB / MKV / 528x240 - https://tls.passthepopcorn.me/torrents.php?id=128247&torrentid=363544 / https://tls.passthepopcorn.me/torrents.php?action=download&id=363544 - sci.fi, thriller
<Hummingbird> Sei donne per l'assassino AKA Blood and Black Lace [1964] by Mario Bava - BD50 / Blu-ray / m2ts / 1080p - https://tls.passthepopcorn.me/torrents.php?id=17010&torrentid=363545 / https://tls.passthepopcorn.me/torrents.php?action=download&id=363545 - thriller, mystery, horror, cult, exploitation, giallo
<Hummingbird> Character Studies [1928] - x264 / DVD / MKV / 716x480 - https://tls.passthepopcorn.me/torrents.php?id=128248&torrentid=363546 / https://tls.passthepopcorn.me/torrents.php?action=download&id=363546 - short
<Hummingbird> Three [2003] by Nick Peterson - x264 / DVD / MKV / 712x480 - https://tls.passthepopcorn.me/torrents.php?id=128249&torrentid=363547 / https://tls.passthepopcorn.me/torrents.php?action=download&id=363547 - short, comedy
<Hummingbird> Hot Girls Wanted [2015] by Jill Bauer and Ronna Gradus - H.264 / WEB / MKV / 720p - https://tls.passthepopcorn.me/torrents.php?id=128250&torrentid=363548 / https://tls.passthepopcorn.me/torrents.php?action=download&id=363548 - documentary
<Hummingbird> Okaeri [1995] by Makoto Shinozaki - H.264 / DVD / MKV / 698x476 - https://tls.passthepopcorn.me/torrents.php?id=128251&torrentid=363549 / https://tls.passthepopcorn.me/torrents.php?action=download&id=363549 - drama
"""
from __future__ import unicode_literals, absolute_import
import re
import requests
from autobit import config
from autobit.db import Release
from autobit.tracker import Tracker
from autobit.classification import MediaClass


class PassThePopcorn(Tracker):

    name = "ptp"
    source_nick = "Hummingbird".lower()
    source_chan = "#ptp-announce-ssl".lower()
    _passkey = ""
    _authkey = ""

    rx = re.compile(r"^(?P<name>.+?)\s-\shttps://.+?torrentid=(?P<id>\d+)")

    def __init__(self):
        super().__init__()
        self.reconfigure()
        self._www_session = requests.Session()
        self._logged_in = False
        self._enabled = False

    def reconfigure(self):
        self._passkey = config['PTP_PASSKEY']
        self._authkey = config['PTP_AUTHKEY']

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

    def verify_source(self, channel: str, nick: str) -> bool:
        return self.source_chan == channel.lower() and self.source_nick == nick.lower()

    def _login(self) -> bool:
        pass

    def _make_torrent_url(self, torrent_id):
        return "http://passthepopcorn.me/torrents.php?action=download&torrent_pass={}&id={}&authkey={}".format(
            self._passkey, torrent_id, config['PTP_AUTHKEY']
        )

    def upload(self, release_name, torrent_file) -> bool:
        pass

    def download(self, release: Release) -> bytes:
        if not self._logged_in and not self.login():
            return None
        r = self._www_session.get(self._make_torrent_url(release.torrent_id))
        if r.ok:
            return r.content
        return False
