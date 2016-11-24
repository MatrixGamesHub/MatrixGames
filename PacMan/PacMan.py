
import mtx
from .Levels import Levels


class PacMan(mtx.Game):

    def GetAuthor():
        return "Tobias Stampfl"

    def GetDescription():
        return """Control Pac-Man through a maze, eating pac-dots. When all pac-dots are eaten, Pac-Man is taken to the next stage."""

    def OnInit(self, settings):
        self._levelNo = -1
        self._dotCount = None
        self._t = 0.0
        self._speed = 8
        self._player = None
        self._nextDirection = None
        self._direction = None

    def GetNextLevel(self):
        if self._levelNo < len(Levels) - 1:
            self._levelNo += 1
            return mtx.Level.CreateByDef(Levels[self._levelNo])
        return None

    def OnLevelStart(self, level, isReset):
        self._player = level.GetPlayer(1)
        self._dotCount = level.GetObjectCount('.')
        self._t = 0.0
        self._nextDirection = None
        self._direction = None

    def OnIdle(self, deltaTime):
        self._t += deltaTime
        threshold = 0.6 - 0.05 * self._speed
        if self._player is not None and self._t > threshold:
                self._t -= threshold

                if self._nextDirection is not None:
                    cell = self.GetAccessibleNeighbourCell(self._player, True, self._nextDirection)
                    if cell is not None:
                        self._direction = self._nextDirection
                        self._nextDirection = None

                if self._direction is not None:
                    self.MovePlayer(1, self._direction)
                    cell = self.GetAccessibleNeighbourCell(self._player, True, self._direction)
                    if cell is None:
                        self._direction = None

    def OnPlayerMoveRequest(self, number, direction):
        if number == 1 and direction != self._nextDirection:
            self._nextDirection = direction

    def OnCollect(self, collectable, source):
        self._dotCount -= 1
        if self._dotCount == 0:
            self.NextLevel()
        return True
