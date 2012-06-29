#
# Copyright (C) 2012 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import os.path


def get_file_extension(file_path):
    """
    >>> get_file_extension("/a/b/c")
    ''
    >>> get_file_extension("/a/b.txt")
    'txt'
    >>> get_file_extension("/a/b/c.tar.xz")
    'xz'
    """
    _ext = os.path.splitext(file_path)[-1]
    if _ext:
        return _ext[1:] if _ext.startswith('.') else _ext
    else:
        return ""


# vim:sw=4:ts=4:et:
