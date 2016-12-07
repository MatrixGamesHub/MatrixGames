
import mtx

Levels = [{'name':    'Level 1',
           'plan':   ['#######',
                      '#1#   #',
                      '# # # #',
                      '#   # #',
                      '### # #',
                      '#t    #',
                      '#######']}]


class Maze(mtx.Game):

    def GetDescription():
        return """Control through a labyrinth, find all the keys and go to the exit to solve the level."""

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
        if source == 'b' and trigger == 't':
            self._solvedCount += 1

            if self._boxCount == self._solvedCount:
                self.NextLevel()

    def OnTriggerLeave(self, trigger, source):
        if source == 'b' and trigger == 't':
            self._solvedCount -= 1
