# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
import unittest
from autobit import classification
from autobit.classification import MediaType


class TestClassification(unittest.TestCase):
    def validate_obj(self, obj, d):
        if hasattr(d, 'items'):
            for k, v in d.items():
                self.assertEqual(getattr(obj, k), v, v)
        else:
            self.assertEqual(obj, d, obj)

    def test_classify_ok(self):
        test_rls = [
            ("The.Hindenburg.1975.1080p.BluRay.x264-PSYCHD", MediaType.MOVIE, {
                "name": "the hindenburg", "resolution": "1080p", "year": 1975}),
            ("Republic.Of.Doyle.S01E02.720p.HDTV.x264-aAF", MediaType.TV, {
                "name": "republic of doyle", "season": 1, "episode": 2, "resolution": "720p"}),
            ("Criterium.du.Dauphine.2015.Stage05.720p.HDTV.x264-WHEELS", MediaType.TV, {
                "name": "criterium du dauphine", "resolution": "720p", "year": 2015})

        ]
        for rls in test_rls:
            self.validate_obj(classification.classify(*rls[0:2]), rls[2])

if __name__ == '__main__':
    unittest.main()
