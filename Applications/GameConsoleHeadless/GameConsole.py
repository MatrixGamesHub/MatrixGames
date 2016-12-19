# encoding: UTF-8
#
# Copyright (C) 2016 Jens Goepfert
#

import sys
sys.path.append("../../../mtxPython/src")
sys.path.append("../../../mtxPython")
sys.path.append("/home/jens/Projects/Python/Phoenix")


import optparse
import os
import time

import mtx
import mtxNet


class ConsoleApp(object):
    
    def __init__(self, gamePath):
        gameLoader = mtx.GameLoader(gamePath)
        gameLoader.Load()
        print(gameLoader.GetGameNames())
        self.gameConsole = mtx.GameConsole()

        self.ctrlHandler = mtxNet.ControllerHandler(self.gameConsole, gameLoader)
        ctrlServer = mtxNet.ControllerServer(50505, self.ctrlHandler)
        ctrlServer.Run()

    
    def MainLoop(self):
        try:
            while 1:
                self.gameConsole.Idle()
                time.sleep(0.01)
        except KeyboardInterrupt:
            pass
        if self.ctrlHandler is not None:
            self.ctrlHandler.DisconnectAllRenderer()


def main():
    ca = ConsoleApp('../../Games')
    ca.MainLoop()


if __name__ == "__main__":
    main()
    