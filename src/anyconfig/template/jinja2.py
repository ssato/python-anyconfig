#
# Jinja2 (http://jinja.pocoo.org) based template renderer.
#
# Copyright (C) Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=wrong-import-position,wrong-import-order
"""anyconfig.template.jinja2_ module.

Template rendering module for jinja2-based template config files.
"""
import pathlib
import os
import typing
import warnings

import jinja2
import jinja2.exceptions

from .. import utils


# .. seealso:: jinja2.loaders.FileSystemLoader.__init__
PathsT = typing.List[typing.Union[str, pathlib.Path]]
MaybePathsT = typing.Optional[PathsT]
MaybeContextT = typing.Optional[typing.Dict[str, typing.Any]]
MaybeFiltersT = typing.Optional[typing.Iterable[typing.Callable]]

RENDER_S_OPTS: typing.List[str] = ['ctx', 'paths', 'filters']
RENDER_OPTS = RENDER_S_OPTS + ['ask']


def tmpl_env(paths: MaybePathsT = None) -> jinja2.Environment:
    """Get the template environment object from given ``paths``.

    :param paths: A list of template search paths
    """
    if paths is None:
        paths = []

    return jinja2.Environment(
        loader=jinja2.FileSystemLoader([str(p) for p in paths])
    )


def make_template_paths(template_file: pathlib.Path,
                        paths: MaybePathsT = None
                        ) -> typing.List[pathlib.Path]:
    """Make a tempalte paths.

    Make up a list of template search paths from given ``template_file`` path
    (absolute or relative path to the template file) and/or ``paths``, a list
    of template search paths given by user or None.

    NOTE: User-given 'paths' will take higher priority over a dir of
    template_file.
    """
    tmpldir = template_file.parent.resolve()
    if paths:
        return [tmpldir] + [pathlib.Path(p) for p in paths
                            if str(p) != str(tmpldir)]

    return [tmpldir]


def render_s(tmpl_s: str, ctx: MaybeContextT = None,
             paths: MaybePathsT = None,
             filters: MaybeFiltersT = None
             ) -> str:
    """Render a template as a str.

    Compile and render given template string 'tmpl_s' with context 'context'.

    :param tmpl_s: Template string
    :param ctx: Context dict needed to instantiate templates
    :param paths: Template search paths
    :param filters: Custom filters to add into template engine
    :return: Compiled result (str)

    >>> render_s('aaa') == 'aaa'
    True
    >>> s = render_s('a = {{ a }}, b = "{{ b }}"', {'a': 1, 'b': 'bbb'})
    >>> assert s == 'a = 1, b = "bbb"'
    """
    if paths is None:
        paths = [os.curdir]

    # .. seealso:: jinja2.environment._environment_sanity_check
    try:
        env = tmpl_env(paths)
    except AssertionError as exc:
        warnings.warn(
            f'Something went wrong with: paths={paths!r}, exc={exc!s}'
        )
        return tmpl_s

    if filters is not None:
        env.filters.update(filters)

    if ctx is None:
        ctx = {}

    return typing.cast(jinja2.Environment, tmpl_env(paths)
                       ).from_string(tmpl_s).render(**ctx)


def render_impl(template_file: pathlib.Path, ctx: MaybeContextT = None,
                paths: MaybePathsT = None, filters: MaybeFiltersT = None
                ) -> str:
    """Render implementation.

    :param template_file: Absolute or relative path to the template file
    :param ctx: Context dict needed to instantiate templates
    :param filters: Custom filters to add into template engine
    :return: Compiled result (str)
    """
    env = tmpl_env(make_template_paths(template_file, paths))  # type: ignore

    if env is None:
        return open(template_file).read()

    if filters is not None:
        env.filters.update(filters)

    if ctx is None:
        ctx = {}

    return env.get_template(pathlib.Path(template_file).name).render(**ctx)


def render(filepath: str, ctx: MaybeContextT = None,
           paths: MaybePathsT = None,
           ask: bool = False,
           filters: MaybeFiltersT = None) -> str:
    """Compile and render template and return the result as a string.

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
    except jinja2.exceptions.TemplateNotFound as mtmpl:
        if not ask:
            raise

        usr_tmpl = input(
            f"{os.linesep}*** Missing template '{mtmpl}'. Please enter "
            "absolute or relative path starts from '.' to the template file: "
        )
        usr_tmpl_2 = pathlib.Path(usr_tmpl.strip()).resolve()
        paths_2 = make_template_paths(usr_tmpl_2, paths)

        return render_impl(usr_tmpl_2, ctx, paths_2, filters)  # type: ignore


def try_render(filepath: typing.Optional[str] = None,
               content: typing.Optional[str] = None,
               **options) -> typing.Optional[str]:
    """Compile and render template and return the result as a string.

    :param filepath: Absolute or relative path to the template file
    :param content: Template content (str)
    :param options: Keyword options passed to :func:`render` defined above.
    :return: Compiled result (str) or None
    """
    if filepath is None and content is None:
        raise ValueError("Either 'path' or 'content' must be some value!")

    try:
        if content is None:
            render_opts = utils.filter_options(RENDER_OPTS, options)
            return render(typing.cast(str, filepath), **render_opts)

        render_s_opts = utils.filter_options(RENDER_S_OPTS, options)
        return render_s(content, **render_s_opts)

    except Exception as exc:  # pylint: disable=broad-except
        if filepath:
            tmpl_s = filepath
        else:
            tmpl_s = typing.cast(str, content)[:10] + ' ...'

        warnings.warn(
            f"Failed to compile '{tmpl_s!r}'. It may not be "
            f'a template.{os.linesep}, exc={exc!s}, '
            f'filepath={filepath}, options={options!r}'
        )
        return None

# vim:sw=4:ts=4:et:
