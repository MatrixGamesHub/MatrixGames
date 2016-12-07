
import sys

import wx
from gui.ImageProvider  import ImageProvider

import mtx
import mtxNet

import imp
Games = imp.load_module('Games', *imp.find_module('Games', ['.', '../..']))


class GameConsoleApp(wx.App):

    def OnInit(self):
        ImageProvider.Init()

        gameConsole = mtx.GameConsole()

        ctrlHandler = mtxNet.ControllerHandler(gameConsole, Games.GameList)
        ctrlServer = mtxNet.ControllerServer(50505, ctrlHandler)
        ctrlServer.Run()

        #ctrlHandler.LoadGame("Sokoban")

        from gui.FrmMain import FrmMain
        frmMain = FrmMain(None, gameConsole=gameConsole, games=Games.GameList)
        frmMain.Show()
        return True


if __name__ == '__main__':
    application = GameConsoleApp(0)
    application.MainLoop()
