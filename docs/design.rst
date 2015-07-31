Philosophy and design principles of anyconfig
==============================================

Philosophy behind anyconfig
-----------------------------

The reason I made anyconfig is aimed to eliminate the need of manual edit of
configuration files, which application developers provide in the applications
orginally, by uesrs. It enables that application developers provide the default
configuration *and* allow users to customize configuration without direct
modification of these configuration files at the same time [#]_ .

There are still many applications force users to edit configuration files
directly if any customization was needed. Sometimes application provides
special configuration tool to hide this fact from users but most tools try to
modify configuration files directly in the end [#]_ .

With using anyconfig or similar library can merge configuraiton files, users of
applications can customize the behavior of applications by just creation of new
configuration files to override the default and there is no need to modify the
default ones.

.. [#] One of examples accomplishing this is systemd; systemd allows users to customize the default provided by unit definitions under /usr/lib/systemd/ by putting unit files under /etc/systemd/. Other examples are sysctl (/etc/sysctl.d/) and sudo (/etc/sudoers.d/).
.. [#] I saw openstack provides such tool, openstack-config; IMHO, the problem should be resolved not by such tools but application design itself, that is, openstack should provide the way to override the default by some configuration files users created newly.

Design principle of anyconfig
-------------------------------

I try to make anyconfig as thin as possible, that is , it works as a thin
wrapper for the backends acutally does configuration load and dump. Thus,
anyconfig does not try to catch any exceptions such as IOError (ex. it failed
to open configuration files) and OSError (ex. you're not allowed to open
configuration files) during load and dump of configuration files. You have to
process these exceptions as needed.

And sometimes backend has specific options for load and dump functions,
therefore, I make anyconfig to pass these options filtered but un-touched.
Filters are statically defined in each backend implementation and maybe lack of
some options. Please feel free to report if you find such backend specific
options not supported in anyconfig's corresponding backend implementation and
I'll make them supported.

.. vim:sw=2:ts=2:et:
