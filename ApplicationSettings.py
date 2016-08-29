#!/usr/bin/env python
import os
import sys
class TxtSettings:
    SettingsPath = ''
    def __init__(self, settingsPath):
        self.SettingsPath = settingsPath
    def Get(self, key):
        with open(self.SettingsPath) as settingsTxtFile:
            for line in settingsTxtFile:
                if line and line.strip().split('=')[0] == key:
                    return line.strip().split('=')[1]

settings = TxtSettings(os.path.dirname(os.path.realpath(sys.argv[0]))+"/Settings.txt")
