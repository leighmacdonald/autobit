# coding=utf-8
"""

"""
import json
import logging
from os.path import dirname, join
from autobit import parser

config = json.load(open(join(dirname(__file__), "config.json")))

logger = logging.getLogger(__name__)

try:
    import znc
except ImportError:
    logger.error("ZNC Module not available")
    znc = None
else:
    # Only load the module if we are using a real ZNC python interpreter with the znc .so module loaded
    class autobit(znc.Module):
        description = "Bittorrent IRC Auto Downloader"
        module_types = [znc.CModInfo.NetworkModule, znc.CModInfo.UserModule]
        args = []
        parser = None
        active = False
        cmd_prefix = "\\"

        def debug(self, msg):
            self.module_msg("DEBUG> {}".format(msg))

        def OnChanMsg(self, nick, channel, message):
            self.debug("OnChanMsg: {}".format(message.s))
            if self.active and self.parser.verify_source(channel.GetName(), nick.GetNick()):
                parsed_line = parser.process_line(self.parser, message.s)
                if not parsed_line:
                    return znc.CONTINUE
                self.module_msg(parsed_line)

            # self.PutModule("Hey, {0} said {1} on {2}".format(nick.GetNick(), message.s, channel.GetName()))
            return znc.CONTINUE

        def OnLoad(self, sArgs, sMessage):
            if sArgs == "tl":
                from autobit.parser.tl import TLParser

                self.parser = TLParser()
            if self.parser:
                self.active = True
                self.module_msg("> Loaded autobit successfully for {}".format(sArgs))
            return self.parser

        def module_msg(self, message):
            self.PutModule("{}".format(message))

        def send_msg(self, target, message):
            self.PutIRC("privmsg {} {}".format(target, message))

from autobit import db

db.make_engine()
