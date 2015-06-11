# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
import enzyme

def parse_video(file_path):
    if file_path.endswith(".mkv"):
        with open(file_path, 'rb') as f:
            info = enzyme.MKV(f)
            return info
