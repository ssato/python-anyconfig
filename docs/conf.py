# -*- coding: utf-8 -*-
#
# pylint:disable=invalid-name
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.resolve() / 'src'))

extensions = ['sphinx.ext.autodoc']
source_suffix = '.rst'
master_doc = 'index'

project = u'python-anyconfig'
copyright = u'2021, Satoru SATOH <satoru.satoh@gmail.com>'
version = '0.10.0'
release = version

exclude_patterns = []

html_theme = 'default'

autodoc_member_order = 'bysource'
