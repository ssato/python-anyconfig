#
# Jinja2 (http://jinja.pocoo.org) based template renderer.
#
# Copyright (C) Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=wrong-import-position,wrong-import-order
"""anyconfig.template module

Template rendering module for jinja2-based template config files.
"""
from __future__ import absolute_import

import codecs
import locale
import pathlib
import os
import typing
import warnings

import anyconfig.utils


RENDER_S_OPTS = ['ctx', 'paths', 'filters']
RENDER_OPTS = RENDER_S_OPTS + ['ask']
SUPPORTED = False
try:
    import jinja2
    from jinja2.exceptions import TemplateNotFound

    SUPPORTED = True

    def tmpl_env(paths):
        """
        :param paths: A list of template search paths
        """
        return jinja2.Environment(loader=jinja2.FileSystemLoader(paths))

except ImportError:
    warnings.warn("Jinja2 is not available on your system, so "
                  "template support will be disabled.")

    class TemplateNotFound(RuntimeError):
        """Dummy exception"""

    def tmpl_env(*_args):
        """Dummy function"""
        return None


def copen(filepath, flag='r', encoding=None):

    """
    FIXME: How to test this ?

    >>> c = copen(__file__)
    >>> c is not None
    True
    """
    if encoding is None:
        encoding = locale.getdefaultlocale()[1]

    return codecs.open(filepath, flag, encoding)


def make_template_paths(template_file: pathlib.Path,
                        paths: typing.Optional[str] = None
                        ) -> typing.List[str]:
    """
    Make up a list of template search paths from given 'template_file'
    (absolute or relative path to the template file) and/or 'paths' (a list of
    template search paths given by user).

    NOTE: User-given 'paths' will take higher priority over a dir of
    template_file.

    :param template_file: Absolute or relative path to the template file
    :param paths: A list of template search paths
    :return: List of template paths ([str])

    >>> make_template_paths("/path/to/a/template")
    ['/path/to/a']
    >>> make_template_paths("/path/to/a/template", ["/tmp"])
    ['/path/to/a', '/tmp']
    >>> os.chdir("/tmp")
    >>> make_template_paths("./path/to/a/template")
    ['/tmp/path/to/a']
    >>> make_template_paths("./path/to/a/template", ["/tmp"])
    ['/tmp/path/to/a', '/tmp']
    """
    tmpldir = str(pathlib.Path(template_file).parent.resolve())
    if paths:
        return [tmpldir] + paths

    return [tmpldir]


def render_s(tmpl_s, ctx=None, paths=None, filters=None):
    """
    Compile and render given template string 'tmpl_s' with context 'context'.

    :param tmpl_s: Template string
    :param ctx: Context dict needed to instantiate templates
    :param paths: Template search paths
    :param filters: Custom filters to add into template engine
    :return: Compiled result (str)

    >>> render_s("aaa") == "aaa"
    True
    >>> s = render_s('a = {{ a }}, b = "{{ b }}"', {'a': 1, 'b': 'bbb'})
    >>> if SUPPORTED:
    ...     assert s == 'a = 1, b = "bbb"'
    """
    if paths is None:
        paths = [os.curdir]

    env = tmpl_env(paths)

    if env is None:
        return tmpl_s

    if filters is not None:
        env.filters.update(filters)

    if ctx is None:
        ctx = {}

    return tmpl_env(paths).from_string(tmpl_s).render(**ctx)


def render_impl(template_file, ctx=None, paths=None, filters=None):
    """
    :param template_file: Absolute or relative path to the template file
    :param ctx: Context dict needed to instantiate templates
    :param filters: Custom filters to add into template engine
    :return: Compiled result (str)
    """
    env = tmpl_env(make_template_paths(template_file, paths))

    if env is None:
        return copen(template_file).read()

    if filters is not None:
        env.filters.update(filters)

    if ctx is None:
        ctx = {}

    return env.get_template(pathlib.Path(template_file).name).render(**ctx)


def render(filepath: str,
           ctx: typing.Optional[typing.Mapping] = None,
           paths: typing.Optional[str] = None,
           ask: bool = False,
           filters: typing.Optional[typing.Callable] = None):
    """
    Compile and render template and return the result as a string.

    :param template_file: Absolute or relative path to the template file
    :param ctx: Context dict needed to instantiate templates
    :param paths: Template search paths
    :param ask: Ask user for missing template location if True
    :param filters: Custom filters to add into template engine
    :return: Compiled result (str)
    """
    fpath = pathlib.Path(filepath)
    try:
        return render_impl(fpath, ctx, paths, filters)
    except TemplateNotFound as mtmpl:
        if not ask:
            raise

        usr_tmpl = input(os.linesep + "*** Missing template "
                         "'{}'. Please enter absolute "
                         "or relative path starting from "
                         "'.' to the template file: ".format(mtmpl))
        usr_tmpl = pathlib.Path(usr_tmpl.strip())
        paths = make_template_paths(usr_tmpl, paths)

        return render_impl(usr_tmpl, ctx, paths, filters)


def try_render(filepath=None, content=None, **options):
    """
    Compile and render template and return the result as a string.

    :param filepath: Absolute or relative path to the template file
    :param content: Template content (str)
    :param options: Keyword options passed to :func:`render` defined above.
    :return: Compiled result (str) or None
    """
    if filepath is None and content is None:
        raise ValueError("Either 'path' or 'content' must be some value!")

    tmpl_s = filepath or content[:10] + " ..."
    try:
        if content is None:
            render_opts = anyconfig.utils.filter_options(RENDER_OPTS, options)
            return render(filepath, **render_opts)
        render_s_opts = anyconfig.utils.filter_options(RENDER_S_OPTS, options)
        return render_s(content, **render_s_opts)
    except Exception as exc:
        warnings.warn("Failed to compile '{}'. It may not be a template.{}"
                      "exc={!r}".format(tmpl_s, os.linesep, exc))
        return None

# vim:sw=4:ts=4:et:
