# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
from subprocess import check_call, CalledProcessError
from os.path import isfile, isdir, join
import logging
import glob
import rarfile

logger = logging.getLogger(__name__)


def make_torrent(path, ann_url, total_size=None, out_name=None, private=True, verbose=True):
    """ For the moment we will probably just use mktorrent since its C based
    and should be a bit faster than a python approach.

    :return:
    :rtype:
    """
    args = ["mktorrent", "-a", ann_url]

    if private:
        args.append("-p")

    if verbose:
        args.append("-v")

    if total_size:
        args.extend(["-l", find_piece_size(total_size)])

    args.append("-o")
    if out_name:
        args.append(out_name)
    else:
        args.append(".".join([path.split("/")[-1], "torrent"]))

    args.append(path)

    logger.debug("Calling mktorrent: {}".format(" ".join(args)))
    try:
        check_call(args)
    except CalledProcessError as err:
        logger.exception("Failed calling mktorrent")
        return False
    else:
        return True


def find_piece_size(total_size):
    """ Determine the ideal piece size for a torrent based on the total
    size of the data being shared.

    :param total_size: Total torrent size
    :type total_size: int
    :return: Piece size (KB)
    :rtype: int
    """
    if total_size <= 2 ** 19:
        return 512
    elif total_size <= 2 ** 20:
        return 1024
    elif total_size <= 2 ** 21:
        return 2048
    elif total_size <= 2 ** 22:
        return 4096
    elif total_size <= 2 ** 23:
        return 8192
    elif total_size <= 2 ** 24:
        return 16384
    else:
        raise ValueError("Total size is unreasonably large")


def extract_release(path):
    if isfile(path):
        return path
    elif isdir(path):
        target = glob.glob(join(path, '*part01.rar'))
        if not target:
            target = glob.glob(join(path, '*part1.rar'))
            if not target:
                target = glob.glob(join(path, '*.rar'))
        if not target:
            raise FileNotFoundError("Could not find suitable target to extract: {}".format(path))
    else:
        raise ValueError("Invalid path, unsupported file type")


def extract_rar(path, target_dir):
    """ Extract *only* the largest file contained within a rar archive. All other
    files are ignored.

    :param path:
    :type path:
    :param target_dir:
    :type target_dir:
    :return:
    :rtype:
    """
    rar = rarfile.RarFile(path, errors="strict")
    try:
        largest = None
        for rar_file in rar.infolist():
            if not largest or rar_file.file_size > largest.file_size:
                largest = rar_file
    except IndexError:
        raise FileNotFoundError("Rar file contains no files")
    else:
        rar.extract(largest, target_dir)
