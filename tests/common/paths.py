#
# Copyright (C) 2023 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Compute paths.
"""
import pathlib
import typing

from . import load


TEST_DATA_MAJOR_VERSION: int = 1

TESTDIR: pathlib.Path = pathlib.Path(__file__).parent.parent.resolve()
RESOURCE_DIR: pathlib.Path = TESTDIR / "res" / str(TEST_DATA_MAJOR_VERSION)


def get_resource_dir(
    loader_or_dumper: str, is_loader: bool = True,
    topdir: typing.Optional[pathlib.Path] = None
) -> pathlib.Path:
    """Top dir to provide test resource data for the loader or dumper.
    """
    return (RESOURCE_DIR if topdir is None else topdir) / (
        "loaders" if is_loader else "dumpers"
    ) / loader_or_dumper


def get_aux_data_paths(
    ipath: pathlib.Path,
    skip_file_exts: typing.Tuple[str, ...] = (".pyc", ),
    **_kwargs
) -> typing.Dict[str, pathlib.Path]:
    """Get a map of subdirs and paths to auxiliary data for input, `ipath`.

    It expects that aux data is in `ipath.parent`/*/.
    """
    name = ipath.name[:-len(ipath.suffix)]  # /a/b/c.json -> c

    return {
        p.parent.name: p for p in ipath.parent.glob(f"*/{name}.*")
        if p.suffix not in skip_file_exts
    }


def get_data(
    topdir: typing.Optional[pathlib.Path],
) -> typing.List[
    typing.Tuple[pathlib.Path, typing.Dict[str, pathlib.Path]]
]:
    # find the dir holding input data files.
    pattern = "*.*"
    if not any(x for x in topdir.iterdir() if x.is_file()):
        pattern = "*/" + pattern

    return sorted(
        (ipath, get_aux_data_paths(ipath))
        for ipath in topdir.glob(pattern) if ipath.is_file()
    )


def load_data(
    topdir: typing.Optional[pathlib.Path],
    **kwargs
) -> typing.List[
    typing.Tuple[pathlib.Path, typing.Dict[str, typing.Any]]
]:
    return [
        (
            ipath,
            {
                subdir: load.load_data(a, **kwargs)
                for subdir, a in adata.items()
            }
        )
        for ipath, adata in get_data(topdir)
    ]
