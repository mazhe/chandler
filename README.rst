Chandler
========

A simple CLI utility displaying OAR cluster information retrieved from the API.

Installation
------------

Requirements:
  - python >= 2.7

You can install, upgrade, uninstall chandler with these commands::

  $ pip install [--user] chandler
  $ pip install [--user] --upgrade chandler
  $ pip uninstall chandler

Or from git (last development version)::

  $ pip install git+https://github.com/oar-team/chandler.git

Or if you already pulled the sources::

  $ pip install path/to/sources

Or if you don't have pip::

  $ easy_install chandler

Configuration
-------------

See the default configuration file: chandler/default_chandler.conf. The file is self-explanatory.

For any customization, copy this file in any of the following locations:
  - /etc/oar/chandler.conf
  - ~/.config/chandler.conf
 Or set the CHANDLER_CONF_FILE environment variable with the location of your choice.
