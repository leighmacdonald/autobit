# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals, absolute_import
import sys
import logging
import glob
from subprocess import check_call, CalledProcessError
from os.path import isfile, isdir, join, abspath
import rarfile

try:
    # Built in for py 3.5+
    from os import scandir
except ImportError:
    try:
        from scandir import scandir
    except ImportError:
        print("Cannot find scandir, please use python 3.5+ or install the scandir package")
        sys.exit(1)

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


def find_rar(path):
    """ This function is designed to find the most appropriate file to use when extracting and/or
    processing releases. This is designed for use with torrent clients and their various "on complete"
    functionality.

    This function will always return the largest file found under a directory, or from the rar file
    itself.

    :param path: Path to search for releases
    :type path:
    :return:
    :rtype:
    """
    if isfile(path):
        return abspath(path)
    elif isdir(path):
        # Find a rar to extract a valid release from
        target = glob.glob(join(path, '*part01.rar'))
        if not target:
            target = glob.glob(join(path, '*part1.rar'))
            if not target:
                target = glob.glob(join(path, '*.rar'))

        if not target:
            # Find the largest non-rar file locatied within the path
            largest = None
            for entry in scandir(path):
                if entry.name.startswith('.'):
                    continue
                if entry.is_file():
                    if largest is None or entry.stat().st_size > largest.stat().st_size:
                        largest = entry
            if not largest:
                raise FileNotFoundError("Could not find suitable target to extract: {}".format(path))
            target = largest.path
        else:
            target = target.pop()
        return target
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
        return join(target_dir, largest.filename)
