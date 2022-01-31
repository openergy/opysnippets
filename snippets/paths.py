"""
opysnippets/paths:1.0.0

Notice
------
all is transformed to posix convention
"""
import os
from pathlib import PurePosixPath, PureWindowsPath


class _OutilPathsError(Exception):
    pass


def get_rel_paths(dir_path):
    """
    dir_path should have been normed (os.normpath)
    """
    rel_paths = set()
    dir_path, dir_names_l, file_names_l = next(os.walk(dir_path))
    for file_name in file_names_l:
        rel_paths.add(file_name)
    for dir_name in dir_names_l:
        for child_rel_path in get_rel_paths(os.path.join(dir_path, dir_name)):
            rel_paths.add(os.path.join(dir_name, child_rel_path))
    return rel_paths


def _normed_pure_path(path):
    """
    Returns
    -------
    normed path (PurePosixPath if no drive, or PureWindowsPath if has drive)

    PureWindowsPath is used because it seems to understand all configuration (\ is not a separator in Posix).
    If has drive, we stay in PureWindowsPath so that c://a.txt is identified as root.
    If not, we then transform to PurePosixPath so that /a.txt is identified as root.

    => we favor Posix, except when there is a drive (which means all normed relative paths are posix)

    We never use PurePath because it will return PurePosixPath or PureWindowsPath depending on the os, which is not
    determinist.
    """
    # test if has drive
    pwp = PureWindowsPath(path)
    if pwp.drive != "":
        return pwp

    return PurePosixPath(pwp.as_posix())


def _ensure(normed_pure_path, relative=False, absolute=False):
    """
    Returns
    -------
    a normed pure path (respecting _normed_pure_path conventions)
    """
    if relative and absolute:
        raise _OutilPathsError("Can't ensure absolute and relative.")

    if relative and normed_pure_path.is_absolute():
        if isinstance(normed_pure_path, PureWindowsPath):
            # normed_pure_path has a drive (see _normed_pure_path definition)
            # since we transform to relative path, we change to PurePosixPath
            normed_pure_path = PurePosixPath(
                normed_pure_path.relative_to(normed_pure_path.drive).as_posix())
        normed_pure_path = normed_pure_path.relative_to("/")
    if absolute and not normed_pure_path.is_absolute():
        # since normed_pure_path.is_absolute(), normed_pure_path is a PosixPurePath
        normed_pure_path = PurePosixPath("/").joinpath(normed_pure_path)
    return normed_pure_path


def universal_path(path, ensure_relative=False, ensure_absolute=False):
    pp = _normed_pure_path(path)
    pp = _ensure(pp, relative=ensure_relative, absolute=ensure_absolute)
    return pp.as_posix()


def universal_join(path, *paths, ensure_relative=False, ensure_absolute=False):
    """
    paths will be changed to relative if they are absolute
    """
    pp = _normed_pure_path(path)
    for _path in paths:
        pp = pp.joinpath(universal_path(_path, ensure_relative=True))
    pp = _ensure(pp, relative=ensure_relative, absolute=ensure_absolute)
    return pp.as_posix()


def get_name(path):
    return _normed_pure_path(path).name
