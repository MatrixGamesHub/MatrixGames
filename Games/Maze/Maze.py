
import mtx
from Levels import levels


class Maze(mtx.Game):

    def OnInit(self, settings):
        self._exit     = None
        self._keyCount = None

    def GetNextLevel(self, number):
        if number <= len(levels):
            return mtx.Level.Create(levels[number - 1])
        return mtx.Level.Create(levels[0], 1)

    def OnLevelStart(self, level, reset):
        self._exit     = level.GetObjects('eE')[0]
        self._keyCount = level.GetObjectCount('k')

    def OnTriggerEnter(self, trigger, source):
        if trigger == 'e':
           self.NextLevel()

    def OnCollect(self, collectable, source):
        if collectable == 'k':
            self._keyCount -= 1
            if self._keyCount == 0:
                self._exit.Unlock()
        return True
