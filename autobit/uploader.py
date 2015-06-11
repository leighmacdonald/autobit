# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
import abc


class Uploader(object):
    @abc.abstractmethod
    def configure(self, config):
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
