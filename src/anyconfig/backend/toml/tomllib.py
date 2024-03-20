#
# Copyright (C) 2023 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# Ref. python -c "import toml; help(toml); ..."
#
r"""A backend module to load and dump TOML files.

- Format to support: TOML, https://github.com/toml-lang/toml
- Requirements: tomli or tomllib and tomli-w
  - tomllib: https://docs.python.org/3/library/tomllib.html
  - tomli: https://github.com/hukkin/tomli
  - tomli-w: https://github.com/hukkin/tomli-w
- Development Status :: 4 - Beta
- Limitations: None obvious
- Special options:
  - tomllib.load{s,} only accept 'parse_float' keyword option.

Changelog:

    .. versionadded:: 0.13.1
"""
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore[no-redef]

import tomli_w

from .. import base


class Parser(base.StringStreamFnParser):
    """TOML parser using tomlib and tomli-w."""

    _cid = "toml.tomllib"
    _type = "toml"
    _extensions = ["toml"]
    _ordered = True
    _load_opts = ["parse_float"]
    _open_read_mode: str = "rb"
    _open_write_mode: str = "wb"

    _load_from_string_fn = base.to_method(tomllib.loads)
    _load_from_stream_fn = base.to_method(tomllib.load)
    _dump_to_string_fn = base.to_method(tomli_w.dumps)
    _dump_to_stream_fn = base.to_method(tomli_w.dump)
