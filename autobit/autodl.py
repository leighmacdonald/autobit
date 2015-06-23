# -*- coding: utf-8 -*-
"""
This module will parse autodl-irssi tracker configs and configure/use them as simple
download only tracker modules.
"""
from __future__ import unicode_literals, absolute_import
import logging
from os.path import exists
try:
    from lxml import etree as ElementTree
except ImportError:
    from xml.etree import ElementTree
from autobit import ConfigError

logger = logging.getLogger()


class AutoDLConfig(object):
    _type = ""
    _short_name = ""
    _settings = {}
    _config_xml = None

    def __init__(self, config_xml):
        if not exists(config_xml):
            raise ConfigError("Cannot read configuration file: {}".format(config_xml))
        self._config_xml = config_xml

    def parse(self):
        parse_ok = False
        try:
            tree = ElementTree.parse(self._config_xml)
            root = tree.getroot()
            for child in root:
                if child.tag == "settings":
                    self._settings = _parse_settings(child)
        except Exception as err:
            logger.exception("Failed to parse autodl config: {}".format(self._config_xml))
        else:
            parse_ok = True
        finally:
            return parse_ok

def _parse_settings(node):
    return [_.attrib for _ in node]
