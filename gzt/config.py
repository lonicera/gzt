#!/usr/bin/python
# -*- coding: utf-8 -*-

import configparser, os

class Settings(object):
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.configFile = os.path.join(os.path.dirname(__file__), 'settings.cfg')

    def write_file(self):
        with open(self.configFile, 'w') as configfile:
            self.config.write(configfile)

    def readSetting(self, item, subitem):
        if not os.path.exists(self.configFile ):
            self.config['main'] = {'update_interval': '60000', 'default_view': 'grid'}
            self.config['newspapers'] = {'list': ''}
            self.write_file()
        else:
            try:
                self.config.read(self.configFile)
                self.config.sections()
                return self.config[item] [subitem]
            except:
                self.config.add_section(item)
                self.config.set(item, subitem, '1')
                self.write_file()
                self.config.read(self.configFile)
                self.config.sections()
                return self.config[item] [subitem]

    def writeSetting(self, item, subitem, value):
        self.config.read(self.configFile)
        self.config.sections()
        self.config[item][subitem] = str(value)
        self.write_file()
