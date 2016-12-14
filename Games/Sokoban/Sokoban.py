
import mtx
from Levels import Levels


class Sokoban(mtx.Game):

    def GetAuthor():
        return "Tobias Stampfl"

    def GetDescription():
        return """Sokoban is a transport puzzle, in which you have to push boxes around in a warehouse, trying to get them to storage locations."""

    def OnInit(self, settings):
        self._boxCount    = None
        self._solvedCount = None

    def GetNextLevel(self, number):
        if number <= len(Levels):
            return mtx.Level.Create(Levels[number - 1])
        return None

    def OnLevelStart(self, level, reset):
        self._boxCount = level.GetObjectCount("b")
        self._solvedCount = level.GetObjectCount("B")

    def OnTriggerEnter(self, trigger, source):
        if trigger == 't' and source == 'b':
            self._solvedCount += 1

            if self._boxCount == self._solvedCount:
                self.NextLevel()

    def OnTriggerLeave(self, trigger, source):
        if trigger == 't' and source == 'b':
            self._solvedCount -= 1
