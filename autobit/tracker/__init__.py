# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
import abc
import logging
import requests
from autobit.db import Release


class Tracker(object):
    """ Base class defining a tracker module that can be sub classed to provide customized
    functionality specific to each tracker being targeted.

    """
    __metaclass__ = abc.ABCMeta

    name = "unknown"

    def __init__(self):
        self.logger = logging.getLogger("tracker.{}".format(self.name))
        self._source_chan = None
        self._source_nick = None
        self.enabled = False
        self.reconfigure()

    @abc.abstractmethod
    def reconfigure(self):
        """ The tracker configuration should be reloaded when this method is called. """
        pass

    @abc.abstractmethod
    def parse_line(self, message: str) -> Release:
        """ Parses a message from IRC for valid release details to parse and potentially download.

        :param message: Raw IRC message to parse.
        :type message: str
        :return: Configured release instance in detached session state.
        :rtype: autobit.db.Release
        """
        pass

    @abc.abstractmethod
    def download(self, release: Release) -> bytes:
        """ Download the supplied release and return the downloaded torrent
        as bytes if successful.

        :param release: Release to download
        :type release: autobit.db.Release
        :return: Downloaded torrent file content
        :rtype: bytes
        """
        pass

    @abc.abstractmethod
    def upload(self, release_name, torrent_file) -> bool:
        """ Upload a torrent to a remote server. This is usually done over
        an api if the receiver has one, otherwise a form upload will
        generally need to be implemented here

        :param torrent_file:
        :type torrent_file:
        :return:
        :rtype:
        """
        pass

    def authenticate(self) -> bool:
        """ If the service requires authentication to be
        established before making an upload, such as a http form behind
        an authenticated session, the authorization portion should override
        this method.

        This method is optional.

        :rtype : bool
        """
        return True

    def verify_source(self, channel: str, nick: str) -> bool:
        return self._source_chan.lower() == channel.lower() and \
               self._source_nick.lower() == nick.lower()

    def _fetch(self, url, headers=None, params=None, verify=True) -> bytes:
        try:
            self.logger.info("Downloading torrent...")
            resp = requests.get(url, headers=headers, params=params, verify=verify)
        except Exception as err:
            self.logger.exception("Failed to fetch torrent")
            return False
        else:
            return resp.content

    def enable(self):
        if not self.enabled:
            self.logger.info("{} tracker enabled".format(self.__class__.__name__))
        self.enabled = True

    def disable(self):
        if self.enabled:
            self.logger.info("{} tracker disabled".format(self.__class__.__name__))
        self.enabled = False

    def make_release(self, name, torrent_id, media_type):
        return Release(name, torrent_id, media_type, self)
