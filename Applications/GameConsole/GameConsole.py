
import os
import sys
import wx

import mtx
import mtxNet

from gui.ImageProvider  import ImageProvider
from Config import Config


class GameConsoleApp(wx.App):

    def OnInit(self):
        ImageProvider.Init()

        config = Config()
        if not config.Load():
            return True

        gameLoader = mtx.GameLoader(config.GamesPath)
        gameConsole = mtx.GameConsole()

        self.ctrlHandler = mtxNet.ControllerHandler(gameConsole, gameLoader)
        ctrlServer = mtxNet.ControllerServer(50505, self.ctrlHandler)
        ctrlServer.Run()

        from gui.FrmMain import FrmMain
        frmMain = FrmMain(None, gameConsole=gameConsole, gameLoader=gameLoader)
        frmMain.Show()
        return True

    def OnExit(self):
        if self.ctrlHandler is not None:
            self.ctrlHandler.DisconnectAllRenderer()
        return wx.App.OnExit(self)


if __name__ == '__main__':
    application = GameConsoleApp(0)
    application.MainLoop()
