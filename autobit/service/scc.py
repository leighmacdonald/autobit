# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
from autobit.irc import IRCParser


class SCCIRCParser(IRCParser):
    """
    > (~SCC@bot.sceneaccess.org): SCC BOT
    > NEW in TV/HD-x264: -> Republic.Of.Doyle.S01E02.720p.HDTV.x264-aAF (Uploaded 2 minutes and 6 seconds after pre) - (1.13 GB) - (https://sceneaccess.eu/details.php?id=1132683)
    """
