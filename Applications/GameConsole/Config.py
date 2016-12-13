
import os
import wx
import configparser
from pathlib import Path

CONFIG_FILENAME = 'Config.ini'
DEFAULT_GAME_DIRECTORIES = ['./Games', '../../Games']


class Config():
    def __init__(self):
        self._gamesPath = None

    def GetGamesPath(self):
        return self._gamesPath
    GamesPath = property(GetGamesPath)

    def DetectGamePath(self):
        root = os.path.dirname(os.path.realpath(__file__))
        for path in DEFAULT_GAME_DIRECTORIES:
            if os.path.isdir(path):
                self._gamesPath = path
                return True

        with wx.MessageDialog(None,
                              message='No games directory found.\n\nPlease select the directory with the '
                                      'matrix games.',
                              caption='Select the games directory',
                              style=wx.OK_DEFAULT | wx.CANCEL) as dlg:
            dlg.OKLabel = 'Select'
            if dlg.ShowModal() == wx.ID_CANCEL:
                return False

        with wx.DirDialog(None, "Select the matrix games directory",
                          defaultPath=root,
                          style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as dlg:
            if dlg.ShowModal() == wx.ID_CANCEL:
                return False

            self._gamesPath = dlg.GetPath()
        return True

    def Load(self):
        self._Read()

        if self._gamesPath is None or not os.path.isdir(self._gamesPath):
            if not self.DetectGamePath():
                return False

        self._Write()
        return True

    def _Read(self):
        if not os.path.isfile(CONFIG_FILENAME):
            return

        config = configparser.ConfigParser()
        config.read(CONFIG_FILENAME)

        self._gamesPath = config.get('GENERAL', 'games directory', fallback=None)

    def _Write(self):
        config = configparser.ConfigParser()
        config['GENERAL'] = {'games directory': self._gamesPath}

        with open(CONFIG_FILENAME, 'w') as configfile:
            config.write(configfile)