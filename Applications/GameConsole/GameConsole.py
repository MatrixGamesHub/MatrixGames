
import os
import sys

import wx
from gui.ImageProvider  import ImageProvider

import mtx
import mtxNet


class GameConsoleApp(wx.App):

    def OnInit(self):
        ImageProvider.Init()

        gameLoader = None

        pathList = ['./Games', '../../Games']
        pathList = []
        for path in pathList:
            if os.path.isdir(path):
                gameLoader = mtx.GameLoader(path)
                break
        else:
            with wx.MessageDialog(None,
                                  message='No games found. Please select the directory with the '
                                          'matrix games.',
                                  caption='Select the games directory',
                                  style=wx.OK_DEFAULT | wx.CANCEL) as dlg:
                dlg.OKLabel = 'Select'
                if dlg.ShowModal() == wx.ID_CANCEL:
                    return True

            with wx.DirDialog(None, "Select the matrix games directory:",
                              defaultPath=os.path.dirname(os.path.realpath(__file__)),
                              style=wx.DD_DEFAULT_STYLE
                                   | wx.DD_DIR_MUST_EXIST) as dlg:
                dlg.CenterOnScreen()
                if dlg.ShowModal() == wx.ID_CANCEL:
                    return True

                gameLoader = mtx.GameLoader(dlg.GetPath())

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
