#!/usr/bin/python
# -*- coding: utf-8 -*-

import configparser
class Settings(object):
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.configFile = 'settings.cfg'
    
    def readSetting(self, item, subitem):
        self.config.read(self.configFile)
        self.config.sections()
        return self.config[item] [subitem]
    
    def writeSetting(self, item, subitem, value):
        self.config.read(self.configFile)
        self.config.sections()
        self.config[item][subitem] = str(value)
        with open(self.configFile, 'w') as configfile:
            self.config.write(configfile)
        
        
#print(Settings().writeSetting('yeniakit','lastId', 700))
        
#print(Settings().readSetting('yeniakit','lastId'))
