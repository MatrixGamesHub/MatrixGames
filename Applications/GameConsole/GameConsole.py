
import os
import sys

import wx
from gui.ImageProvider  import ImageProvider

import mtx
import mtxNet


class GameConsoleApp(wx.App):

    def OnInit(self):
        ImageProvider.Init()

        gameLoader = mtx.GameLoader('./Games', '../../Games')
        gameConsole = mtx.GameConsole()

        ctrlHandler = mtxNet.ControllerHandler(gameConsole, gameLoader)
        ctrlServer = mtxNet.ControllerServer(50505, ctrlHandler)
        ctrlServer.Run()

        #ctrlHandler.LoadGame("Sokoban")

        from gui.FrmMain import FrmMain
        frmMain = FrmMain(None, gameConsole=gameConsole, gameLoader=gameLoader)
        frmMain.Show()
        return True


if __name__ == '__main__':
    application = GameConsoleApp(0)
    application.MainLoop()
