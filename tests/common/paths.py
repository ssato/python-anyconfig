#
# Copyright (C) 2023 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Compute paths.
"""
import pathlib
import typing


TEST_DATA_MAJOR_VERSION: int = 1

TESTDIR: pathlib.Path = pathlib.Path(__file__).parent.parent.resolve()
RESOURCE_DIR: pathlib.Path = TESTDIR / "res" / str(TEST_DATA_MAJOR_VERSION)

EXTS_TO_TRY: typing.Tuple[str, ...] = (
    "json",
    "py",
    "pickle",
)


def get_resource_dir(
    loader_or_dumper: str, is_loader: bool = True,
    topdir: typing.Optional[pathlib.Path] = None
) -> pathlib.Path:
    """Top dir to provide test resource data for the loader or dumper.
    """
    return (RESOURCE_DIR if topdir is None else topdir) / (
        "loaders" if is_loader else "dumpers"
    ) / loader_or_dumper


def get_expected_data_path(
    ipath: pathlib.Path,
    file_ext: typing.Union[str, bool] = False,
    exts_to_try: typing.Tuple[str, ...] = EXTS_TO_TRY,
    **_kwargs
) -> typing.Optional[pathlib.Path]:
    """Get a path to expected data for input, `ipath`.
    """
    if file_ext:
        candidate = ipath.parent / "e" / f"{ipath.name}.{file_ext}"
        if candidate.exists():
            return candidate

    for ext in exts_to_try:
        candidate = ipath.parent / "e" / f"{ipath.name}.{ext}"
        if candidate.exists():
            return candidate

    return None


def get_data_path_pairs(
    loader_or_dumper: str, is_loader: bool = True,
    file_ext: typing.Union[str, bool] = False,
    exts_to_try: typing.Tuple[str, ...] = EXTS_TO_TRY,
    topdir: typing.Optional[pathlib.Path] = None,
    **_kwargs
) -> typing.List[typing.Tuple[pathlib.Path, pathlib.Path]]:
    """Get a path to expected data for input, `ipath`.
    """
    resdir = get_resource_dir(
        loader_or_dumper, is_loader=is_loader, topdir=topdir
    )
    return sorted(
        (
            ipath,
            get_expected_data_path(
                ipath, file_ext=file_ext, exts_to_try=exts_to_try
            )
        )
        for ipath in resdir.glob("*/*.*") if ipath.is_file()
    )
