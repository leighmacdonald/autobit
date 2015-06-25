# -*- coding: utf-8 -*-
"""
This module will parse autodl-irssi tracker configs and configure/use them as simple
download only tracker modules.
"""
from __future__ import unicode_literals, absolute_import
import re
from os.path import exists
import xmltodict
from autobit import ConfigError
from autobit.tracker import Tracker
from autobit.db import Release


class AutoDLParser(Tracker):
    """
    This class attempts to read in autodl-irssi config files (xml) and parse the needed
    details from it to allow downloading from trackers that are not fully supported by
    autobit.

    Note that these configs only allow the download functionality to be used. If you want
    to create a fully supported tracker instance you will probably want to subclass
    autobit.tracker.Tracker and create your own implementation.
    """
    _config_xml = None
    _data = {}
    _rx = None
    _rx_vars = []

    def __init__(self, config_xml):

        if not exists(config_xml):
            raise ConfigError("Cannot read configuration file: {}".format(config_xml))
        self._config_xml = config_xml

        # Call last since we need to configure xml settings before invoking reconfigure()
        super().__init__()

    def reconfigure(self):
        self._data = xmltodict.parse(open(self._config_xml).read())
        try:
            rx = self._data['trackerinfo']['parseinfo']['linepatterns']['extract']['regex']['@value']
            self._rx_vars.clear()
            for var in self._data['trackerinfo']['parseinfo']['linepatterns']['extract']['vars']['var']:
                self._rx_vars.append(var['@name'])
        except KeyError:
            self.disable()
        else:
            self._rx = re.compile(rx, re.IGNORECASE)
            self.enable()



    def upload(self, release_name, torrent_file) -> bool:
        raise NotImplementedError()

    def parse_line(self, message: str) -> Release:
        pass

    def download(self, release: Release) -> bytes:
        pass
