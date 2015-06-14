# -*- coding: utf-8 -*-
"""
This file contains all the core default settings used in the application.

You should *not* change these values, instead overwrite them in your own
settings.py file path set using the AUTOBIT_SETTINGS env var like so:

AUTOBIT_SETTINGS=/home/user/my_settings.py python3 autobit.py

"""
from __future__ import unicode_literals, absolute_import
from os.path import expanduser

# Application paths

# Where the torrent client will pick up releases
WATCH_DIR = expanduser("~/.config/autobit/watch")

# Tracker configurations
BTN_ENABLE_UPLOAD = False
BTN_ENABLE_DOWNLOAD = False
BTN_AUTHKEY = ""
BTN_PASSKEY = ""

TOTV_ENABLE_UPLOAD = False
TOTV_ENABLE_DOWNLOAD = False
TOTV_APIKEY = ""

PTN_ENABLE_UPLOAD = False
PTN_ENABLE_DOWNLOAD = False
PTN_USER = ""
PTN_PASS = ""

SCC_ENABLE_UPLOAD = False
SCC_ENABLE_DOWNLOAD = False
SCC_PASSKEY = ""

TL_SOURCE_NICK = "_AnnounceBot_".lower()
TL_SOURCE_CHAN = "#tlannounces".lower()
TL_APIKEY = ""

PTP_PASSKEY = ""
PTP_AUTHKEY = ""
