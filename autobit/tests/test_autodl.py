# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
import unittest
from os.path import join
from autobit.autodl import AutoDLConfig
from autobit.tests import fixture_root


class AutoDLTest(unittest.TestCase):
    config_root = join(fixture_root, "autodl")

    def test_parse(self):
        single_line = join(self.config_root, "singleline.tracker")
        multi_line = join(self.config_root, "multiline.tracker")
        parser = AutoDLConfig(single_line)
        try:
            parser.parse()
        except:
            self.fail("Error parsing config")
        else:
            self.assertTrue(parser)


if __name__ == '__main__':
    unittest.main()
