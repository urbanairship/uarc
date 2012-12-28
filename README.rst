uarc
====

A Python library for reading ``uarc`` files. ``uarc`` files contain aliases and
information for common Urban Airship data such as apps, secrets, and device
identifiers. Tools may use these aliases to avoid making users remember
randomly generated identifiers.


uarc Files
----------

``uarc`` files are simple ini-style files (`SafeConfigParser`_ compatible) such as:

.. sourcecode:: ini

   [MyApp]
   key=...
   secret=...
   apid.foo=...
   pin.bar=...
   token.egg=...
   token.spam=...

The section name ``MyApp`` is the alias for an app. Each app may specify its
key and secrets as well as any number of device aliases. 

Files are loaded in the following order:

1. ``/etc/ua/uarc`` - System-wide
1. ``$HOME/.uarc`` - User-specific
1. ``$PWD/.uarc`` - Directory-specific
1. ``$UARC`` - Custom

Files loaded last overwrite earlier read files.

.. _SafeConfigParser: http://docs.python.org/2/library/configparser.html
