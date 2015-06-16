# coding=utf-8
"""

"""
import logging
from os.path import dirname, exists
from flask.config import Config
import os


logger = logging.getLogger(__name__)


class AutoBitError(Exception):
    pass


class TrackerError(AutoBitError):
    pass


class ConfigError(AutoBitError):
    pass


def load_config():
    cfg = Config(dirname(dirname(__file__)))
    cfg.from_object("autobit.settings")
    if "AUTOBIT_SETTINGS" in os.environ:
        cfg.from_envvar("AUTOBIT_SETTINGS")

    if not exists(cfg['WATCH_DIR']):
        logger.info("Creating watch dir: {}".format(cfg['WATCH_DIR']))
        os.makedirs(cfg['WATCH_DIR'])

    return cfg

config = load_config()

# This is here due to the way znc loads modules.
# TODO confirm if this is actually true
try:
    import znc
except ImportError:
    logger.warning("Python ZNC Module not available")
    znc = None
else:
    # Only load the module if we are using a real ZNC python interpreter with the znc .so module loaded
    # If this is not like this it makes testing a pain.

    class autobit(znc.Module):
        """
        This is the ZNC module that will parse incoming IRC messages
        """
        description = "Bittorrent IRC Auto Downloader"
        module_types = [znc.CModInfo.GlobalModule, znc.CModInfo.NetworkModule, znc.CModInfo.UserModule]
        args = []
        tracker = None
        active = False
        cmd_prefix = "\\"

        def debug(self, msg):
            self.module_msg("DEBUG> {}".format(msg))

        def OnChanMsg(self, nick, channel, message):
            self.debug("OnChanMsg: {}".format(message.s))
            if self.active and self.tracker.verify_source(channel.GetName(), nick.GetNick()):
                parsed_line = self.tracker.parse_line(message.s)
                if not parsed_line:
                    return znc.CONTINUE
                self.module_msg(parsed_line)

            # self.PutModule("Hey, {0} said {1} on {2}".format(nick.GetNick(), message.s, channel.GetName()))
            return znc.CONTINUE

        def OnLoad(self, sArgs, sMessage):
            self.module_msg("Loading..")
            if sArgs == "tl":
                from autobit.tracker.tl import TorrentLeech

                self.tracker = TorrentLeech()
            if self.tracker:
                self.active = True
                self.module_msg("> Loaded autobit successfully for {}".format(sArgs))
            return self.tracker

        def module_msg(self, message):
            self.PutModule("{}".format(message))

        def send_msg(self, target, message):
            self.PutIRC("privmsg {} {}".format(target, message))

from autobit import db

db.make_engine()
