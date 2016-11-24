
import mtx
import random

from .Levels import Levels


class Wesp(mtx.Game):

    def GetAuthor():
        return "Tobias Stampfl"

    def GetDescription():
        return """Wesp is an elimination puzzles, in which you have to move or jump on tiles to eliminate them until all tiles are gone."""

    def OnInit(self, settings):
        self._levelNo = -1
        self._tileCount = None

        settings.cellAccessWhitelist = '+'

    def GetNextLevel(self):
        #return self._GenerateLevel(8, 8, 15, 2)
        if self._levelNo < len(Levels) - 1:
            self._levelNo += 1
            return mtx.Level.CreateByDef(Levels[self._levelNo])
        return None

    def OnLevelStart(self, level, isReset):
        self._tileCount = level.GetObjectCount("+")

    def OnRemove(self, removable, source):
        self._tileCount -= 1
        if self._tileCount == 1:
            self.NextLevel()
        return True

    def _GenerateLevel(self, width, height, tileCount, maxTileLayerDepth, startPosition=None):

        if startPosition is None:
            startX = x = random.randrange(width)
            startY = y = random.randrange(height)
        else:
            startX = x = startPosition.x
            startY = y = startPosition.y

        level = mtx.Level(width, height, 'Random')

        level.Add(x, y, '+')

        for __ in range(tileCount - 1):
            cell = None

            while cell is None or cell.GetObjectCount('+') == maxTileLayerDepth:
                distance = random.randrange(1, 3)
                direction = random.randrange(4)

                if direction == mtx.LEFT:
                    cell = level.GetCell(x - distance, y)

                elif direction == mtx.RIGHT:
                    cell = level.GetCell(x + distance, y)

                elif direction == mtx.UP:
                    cell = level.GetCell(x, y - distance)

                elif direction == mtx.DOWN:
                    cell = level.GetCell(x, y + distance)

            x = cell._x
            y = cell._y
            level.Add(x, y, '+')

        level.Add(startX, startY, '1')

        return level