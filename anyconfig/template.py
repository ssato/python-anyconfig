#
# Jinja2 (http://jinja.pocoo.org) based template renderer.
#
# Author: Satoru SATOH <ssato redhat.com>
# License: MIT
#
"""Template rendering module for jinja2-based template config files.
"""
from __future__ import absolute_import

import jinja2
import os

import anyconfig.compat


def tmpl_env(paths):
    """
    :param paths: A list of template search paths
    """
    return jinja2.Environment(loader=jinja2.FileSystemLoader(paths))


def make_template_paths(template_file, paths=None):
    """
    Make up a list of template search paths from given `template_file`
    (absolute or relative path to the template file) and/or `paths` (a list of
    template search paths given by user).

    NOTE: User-given `paths` will take higher priority over a dir of
    template_file.

    :param template_file: Absolute or relative path to the template file
    :param paths: A list of template search paths

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

    >>> s = render_s('a = {{ a }}, b = "{{ b }}"', {'a': 1, 'b': 'bbb'})
    >>> s == 'a = 1, b = "bbb"'
    True
    """
    if paths is None:
        paths = [os.curdir]

    env = tmpl_env(paths)

    if env is None:
        return tmpl_s
    else:
        if ctx is None:
            ctx = {}

        return tmpl_env(paths).from_string(tmpl_s).render(**ctx)


def render_impl(template_file, ctx=None, paths=None):
    """
    :param template_file: Absolute or relative path to the template file
    :param ctx: Context dict needed to instantiate templates
    """
    env = tmpl_env(make_template_paths(template_file, paths))

    if env is None:
        return anyconfig.compat.copen(template_file).read()
    else:
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
    """
    try:
        return render_impl(filepath, ctx, paths)
    except jinja2.TemplateNotFound as mtmpl:
        if not ask:
            raise RuntimeError("Template Not found: " + str(mtmpl))

        usr_tmpl = anyconfig.compat.raw_input("\n*** Missing template "
                                              "'%s'. Please enter absolute "
                                              "or relative path starting from "
                                              "'.' to the template file: " %
                                              mtmpl)
        usr_tmpl = os.path.normpath(usr_tmpl.strip())
        paths = make_template_paths(usr_tmpl, paths)

        return render_impl(usr_tmpl, ctx, paths)

# vim:sw=4:ts=4:et:
