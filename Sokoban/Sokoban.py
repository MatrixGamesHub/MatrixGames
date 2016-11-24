
import mtx
from .Levels import Levels


class Sokoban(mtx.Game):

    def GetAuthor():
        return "Tobias Stampfl"

    def GetDescription():
        return """Sokoban is a transport puzzle, in which you have to push boxes around in a warehouse, trying to get them to storage locations."""

    def OnInit(self, settings):
        self._levelNo     = -1
        self._boxCount    = None
        self._solvedCount = None

    def GetNextLevel(self):
        if self._levelNo < len(Levels) - 1:
            self._levelNo += 1
            return mtx.Level.CreateByDef(Levels[self._levelNo])
        return None

    def OnLevelStart(self, level, isReset):
        self._boxCount = level.GetObjectCount("b")
        self._solvedCount = level.GetObjectCount("B")

    def OnTriggerEnter(self, trigger, source):
        if source.Is('b') and trigger.Is('t'):
            self._solvedCount += 1

            if self._boxCount == self._solvedCount:
                self.NextLevel()

    def OnTriggerLeave(self, trigger, source):
        if source.Is('b') and trigger.Is('t'):
            self._solvedCount -= 1





#        ld = {'name':    'Level 1',
#              'ground':  mtx.TEXTURE.GROUND.EARTH,
#              'wall':    mtx.TEXTURE.WALL.RED_BRICKS,
#              'plan':   ['#####################',
#                         '#                   #',
#                         '#          t        #',
#                         '# ttt tt  tttt t  t #',
#                         '# t  t  t  t    tt  #',
#                         '# t  t  t  t   t  t #',
#                         '# t  t  t   tt t  t #',
#                         '#                   #',
#                         '#####################']}
#              'plan':   ['###################################################',
#                         '#                                                 #',
#                         '#          t        bbb        b   b              #',
#                         '# ttt tt  tttt t  t b  b b  b bbbb bbb   bb  bbb  #',
#                         '# t  t  t  t    tt  bbb  b  b  b   b  b b  b b  b #',
#                         '# t  t  t  t   t  t b    b  b  b   b  b b  b b  b #',
#                         '# t  t  t   tt t  t b     bbb   bb b  b  bb  b  b #',
#                         '#                           b                     #',
#                         '#                         bb                      #',
#                         '#                                                 #',
#                         '###################################################']}
#
#        return mtx.Level.CreateByDef(ld)
