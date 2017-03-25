#
# Jinja2 (http://jinja.pocoo.org) based template renderer.
#
# Author: Satoru SATOH <ssato redhat.com>
# License: MIT
#
# pylint: disable=unused-argument,wrong-import-position,wrong-import-order
"""anyconfig.template module

Template rendering module for jinja2-based template config files.
"""
from __future__ import absolute_import

import codecs
import locale
import logging
import os

import anyconfig.compat

LOGGER = logging.getLogger(__name__)
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
    LOGGER.warning("Jinja2 is not available on your system, so "
                   "template support will be disabled.")

    class TemplateNotFound(RuntimeError):
        """Dummy exception"""
        pass

    def tmpl_env(*args):
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


def make_template_paths(template_file, paths=None):
    """
    Make up a list of template search paths from given `template_file`
    (absolute or relative path to the template file) and/or `paths` (a list of
    template search paths given by user).

    NOTE: User-given `paths` will take higher priority over a dir of
    template_file.

    :param template_file: Absolute or relative path to the template file
    :param paths: A list of template search paths
    :return: List of template paths ([str])

    >>> make_template_paths("/path/to/a/template")
    ['/path/to/a']
    >>> make_template_paths("/path/to/a/template", ["/tmp"])
    ['/tmp', '/path/to/a']
    >>> os.chdir("/tmp")
    >>> make_template_paths("./path/to/a/template")
    ['/tmp/path/to/a']
    >>> make_template_paths("./path/to/a/template", ["/tmp"])
    ['/tmp', '/tmp/path/to/a']
    """
    tmpldir = os.path.abspath(os.path.dirname(template_file))
    return [tmpldir] if paths is None else paths + [tmpldir]


def render_s(tmpl_s, ctx=None, paths=None):
    """
    Compile and render given template string `tmpl_s` with context `context`.

    :param tmpl_s: Template string
    :param ctx: Context dict needed to instantiate templates
    :param paths: Template search paths
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

    if ctx is None:
        ctx = {}

    return tmpl_env(paths).from_string(tmpl_s).render(**ctx)


def render_impl(template_file, ctx=None, paths=None):
    """
    :param template_file: Absolute or relative path to the template file
    :param ctx: Context dict needed to instantiate templates
    :return: Compiled result (str)
    """
    env = tmpl_env(make_template_paths(template_file, paths))

    if env is None:
        return copen(template_file).read()

    if ctx is None:
        ctx = {}

    return env.get_template(os.path.basename(template_file)).render(**ctx)


def render(filepath, ctx=None, paths=None, ask=False):
    """
    Compile and render template and return the result as a string.

    :param template_file: Absolute or relative path to the template file
    :param ctx: Context dict needed to instantiate templates
    :param paths: Template search paths
    :param ask: Ask user for missing template location if True
    :return: Compiled result (str)
    """
    try:
        return render_impl(filepath, ctx, paths)
    except TemplateNotFound as mtmpl:
        if not ask:
            raise

        usr_tmpl = anyconfig.compat.raw_input(os.linesep + ""
                                              "*** Missing template "
                                              "'%s'. Please enter absolute "
                                              "or relative path starting from "
                                              "'.' to the template file: " %
                                              mtmpl)
        usr_tmpl = os.path.normpath(usr_tmpl.strip())
        paths = make_template_paths(usr_tmpl, paths)

        return render_impl(usr_tmpl, ctx, paths)


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
    LOGGER.debug("Compiling: %s", tmpl_s)
    try:
        if content is None:
            return render(filepath, **options)
        else:
            return render_s(content, **options)
    except Exception as exc:
        LOGGER.warning("Failed to compile '%s'. It may not be a template.%s"
                       "exc=%r", tmpl_s, os.linesep, exc)
        return None

# vim:sw=4:ts=4:et:
