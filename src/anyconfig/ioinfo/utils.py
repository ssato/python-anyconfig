#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Utility funtions for anyconfig.ionfo."""
import itertools
import pathlib
import typing

from .constants import GLOB_MARKER, PATH_SEP


def get_path_and_ext(path: pathlib.Path) -> typing.Tuple[pathlib.Path, str]:
    """Normaliez path objects and retunr it with file extension."""
    abs_path = path.expanduser().resolve()
    file_ext = abs_path.suffix
    return (
        abs_path,
        file_ext[1:] if file_ext.startswith('.') else ''
    )


def expand_from_path(path: pathlib.Path,
                     marker: str = GLOB_MARKER
                     ) -> typing.Iterator[pathlib.Path]:
    """Expand ``path`` contains '*' in its path str."""
    if not path.is_absolute():
        path = path.resolve()

    idx_part = list(
        enumerate(itertools.takewhile(lambda p: marker not in p, path.parts))
    )[-1]

    if not idx_part:
        raise ValueError(f'It should not happen: {path!r}')

    idx = idx_part[0] + 1
    if len(path.parts) > idx:
        base = pathlib.Path(path.parts[0]).joinpath(*path.parts[:idx])
        pattern = PATH_SEP.join(path.parts[idx:])
        for epath in sorted(base.glob(pattern)):
            yield epath

    else:  # No marker was found.
        yield path

# vim:sw=4:ts=4:et:
