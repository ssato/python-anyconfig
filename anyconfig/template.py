#
# Jinja2 (http://jinja.pocoo.org) based template renderer.
#
# Author: Satoru SATOH <ssato redhat.com>
# License: MIT
#
from anyconfig.compat import raw_input, copen
from anyconfig.globals import LOGGER

import os.path
import os

TEMPLATE_SUPPORT = False
try:
    import jinja2
    from jinja2.exceptions import TemplateNotFound

    TEMPLATE_SUPPORT = True

    def tmpl_env(paths):
        return jinja2.Environment(loader=jinja2.FileSystemLoader(paths))

except ImportError:
    LOGGER.warn("Jinja2 is not available on your system, so "
                "template support will be disabled.")

    class TemplateNotFound(RuntimeError):
        pass

    def tmpl_env(paths):
        return None


def make_template_paths(template_file, paths=[]):
    """
    :param template_file: Absolute or relative path to the template file
    :param paths: A list of template search paths

    >>> make_template_paths("/path/to/a/template")
    ['.', '/path/to/a']
    >>> make_template_paths("/path/to/a/template", ["/tmp", "."])
    ['/tmp', '.', '/path/to/a']
    """
    tmpldir = os.path.abspath(os.path.dirname(template_file))
    return paths + [tmpldir] if paths else [os.curdir, tmpldir]


def render_s(tmpl_s, ctx={}, paths=[os.curdir]):
    """
    Compile and render given template string `tmpl_s` with context `context`.

    :param tmpl_s: Template string
    :param ctx: Context dict needed to instantiate templates
    :param paths: Template search paths

    >>> s = render_s('a = {{ a }}, b = "{{ b }}"', {'a': 1, 'b': 'bbb'})
    >>> if TEMPLATE_SUPPORT:
    ...     assert s == 'a = 1, b = "bbb"'
    """
    env = tmpl_env(paths)

    if env is None:
        return tmpl_s
    else:
        return tmpl_env(paths).from_string(tmpl_s).render(**ctx)


def render_impl(template_file, ctx={}, paths=[]):
    """
    :param template_file: Absolute or relative path to the template file
    :param ctx: Context dict needed to instantiate templates
    """
    env = tmpl_env(make_template_paths(template_file, paths))

    if env is None:
        return copen(template_file).read()
    else:
        return env.get_template(os.path.basename(template_file)).render(**ctx)


def render(filepath, ctx={}, paths=[], ask=False):
    """
    Compile and render template and return the result as a string.

    :param template_file: Absolute or relative path to the template file
    :param ctx: Context dict needed to instantiate templates
    :param paths: Template search paths
    :param ask: Ask user for missing template location if True
    """
    try:
        return render_impl(filepath, ctx, paths)
    except TemplateNotFound as mtmpl:
        if not ask:
            raise RuntimeError("Template Not found: " + str(mtmpl))

        usr_tmpl = raw_input("\n*** Missing template '%s'. "
                             "Please enter absolute or relative path "
                             "starting from '.' to the template "
                             "file: " % mtmpl)
        usr_tmpl = os.path.normpath(usr_tmpl.strip())
        usr_tmpldir = os.path.dirname(usr_tmpl)

        return render_impl(usr_tmpl, ctx, paths + [usr_tmpldir])

# vim:sw=4:ts=4:et:
