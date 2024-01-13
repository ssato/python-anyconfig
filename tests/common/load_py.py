#
# Copyright (C) 2023, 2024 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Load data from .py
"""
import ast
import importlib
import importlib.abc
import pathlib
import typing
import warnings


DATA_VAR_NAME: str = "DATA"


def load_literal_data_from_string(content: str) -> typing.Any:
    """Load test data expressed by literal data string ``content``."""
    return ast.literal_eval(content)


def load_literal_data_from_path(path: pathlib.Path) -> typing.Any:
    """Load test data expressed by literal data from .py files.

    .. note:: It should be safer than the above function.
    """
    return load_literal_data_from_string(path.read_text().strip())


def load_data_from_py(
    path: pathlib.Path,
    data_name: typing.Optional[str] = None,
    safe: bool = False
) -> typing.Any:
    """Load test data from .py files by evaluating it.

    .. note:: It's not safe.
    """
    if data_name is None:
        data_name = DATA_VAR_NAME

    spec = importlib.util.spec_from_file_location('testmod', str(path))
    if spec and isinstance(spec.loader, importlib.abc.Loader):
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        try:
            return getattr(mod, data_name)
        except (TypeError, ValueError, AttributeError):
            warnings.warn(  # noqa
                f'No valid data "{data_name}" was found in {mod!r}.'
            )

    if safe:
        return None

    raise ValueError(f"Faied to load data from: {path!r}")


def load_from_path(
    path: pathlib.Path,
    data_name: typing.Optional[str] = None,
    safe: bool = False
) -> typing.Any:
    """Load data from given path `path`. It will choose the appropriate
    function by the keyword, `data_name`, in the content of the file.
    """
    if (data_name or DATA_VAR_NAME) in path.read_text():
        return load_data_from_py(path, data_name=data_name, safe=safe)

    return load_literal_data_from_path(path)
