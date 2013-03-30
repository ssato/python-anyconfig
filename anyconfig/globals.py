#
# Copyright (C) 2013 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import logging
import os


AUTHOR = 'Satoru SATOH <ssat@redhat.com>'
VERSION = "0.0.3.8"

# For daily snapshot versioning mode:
if os.environ.get("_ANYCONFIG_SNAPSHOT_BUILD", None) is not None:
    import datetime
    VERSION = VERSION + datetime.datetime.now().strftime(".%Y%m%d")

# Setup logger:
_LOGGING_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

logging.basicConfig(level=logging.WARNING, format=_LOGGING_FORMAT)

LOGGER = logging.getLogger("anyconfig")

sh = logging.StreamHandler()
sh.setLevel(logging.WARNING)
sh.setFormatter(logging.Formatter(_LOGGING_FORMAT))

LOGGER.addHandler(sh)

# vim:sw=4:ts=4:et:
