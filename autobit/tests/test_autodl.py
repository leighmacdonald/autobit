# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
import unittest
from os.path import join
from autobit.tracker.autodl import AutoDLParser
from autobit.tests import fixture_root


class AutoDLTest(unittest.TestCase):
    config_root = join(fixture_root, "autodl")

    def test_parse(self):
        tests = [
            [
                join(self.config_root, "singleline.tracker"),
                "| Blackcats 2.2: New Torrent  'Pajama.Sam.No.Need.To.Hide.When.Its.Dark.Outside' in 'PC'  "
                "has been uploaded by 'd3xtro' | http://www.blackcats-games.net/details.php?id=43900&hit=1"],
            [
                join(self.config_root, "multiline.tracker"),
                "New Upload: Stargate.Universe.S01.Vol1.720p.BluRay.x264-SiNNERS\n"
                "Category: TV-DVDRIP\n"
                "URL: http://www.acetorrents.net/details.php?id=72139 "]
        ]
        for config_path, irc_line in tests:
            try:
                parser = AutoDLParser(config_path)
                parser.parse_line(irc_line)
            except:
                self.fail("Error parsing config")
            else:

                self.assertTrue(parser)


if __name__ == '__main__':
    unittest.main()
