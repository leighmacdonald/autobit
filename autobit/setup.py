#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='autobit',
    version='0.1',
    description='ZNC/IRC Based torrent auto downloader and uploader',
    author='Leigh MacDonald',
    url="https://github.com/leighmacdonald/autobit",
    author_email='leigh.macdonald@gmail.com',
    packages=['autobit', 'autobit.tracker'],
)
