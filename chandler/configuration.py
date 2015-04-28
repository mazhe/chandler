# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import pprint
import ConfigParser


class Configuration(ConfigParser.ConfigParser):
    DEFAULT_CONFIG_FILES = [
        os.path.join(os.environ['HOME'], '.config', 'chandler.conf'),
        os.path.join('/etc', 'oar', 'chandler.conf'),
    ]

    def __init__(self):
        if os.environ.get('CHANDLER_CONF_FILE', None):
            env_file = os.environ['CHANDLER_CONF_FILE']
            self.DEFAULT_CONFIG_FILES.insert(0, env_file)
        ConfigParser.ConfigParser.__init__(self, allow_no_value=False)
        for config_file in self.DEFAULT_CONFIG_FILES[:-1]:
            if self.load_file(config_file, silent=True):
                break
        else:
            self.load_file(self.DEFAULT_CONFIG_FILES[-1], silent=False)

    def load_file(self, filename, silent=False):
        """Updates the values in the config from a config file.
        :param filename: the filename of the config.  This can either be an
                         absolute filename or a filename relative to the
                         root path.
        """
        try:
            with open(filename) as f:
                self.readfp(f)
        except IOError as e:
            if silent:
                return False
            e.strerror = ('Unable to load configuration file. \n\n'
                          'The configuration file is searched into %s or in '
                          'the location given by the $CHANDLER_CONF_FILE '
                          'environement variable' % self.DEFAULT_CONFIG_FILES)
            raise
        return True

    def __str__(self):
        return pprint.pprint(self._sections)
