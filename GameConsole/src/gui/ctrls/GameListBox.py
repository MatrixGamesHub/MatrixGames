
import wx
from gui.lib.Common import ColourGradient

GameSelectEvent, EVT_GAME_SELECT = wx.lib.newevent.NewEvent()
GameStartEvent, EVT_GAME_START = wx.lib.newevent.NewEvent()
GameStopEvent, EVT_GAME_STOP = wx.lib.newevent.NewEvent()


class GameListBox(wx.VListBox):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
                  name=wx.VListBoxNameStr, games=None):
        wx.VListBox.__init__(self, parent, id, pos, size, style | wx.NO_BORDER, name)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self._OnActivate)
        self.Bind(wx.EVT_LISTBOX, self._OnSelect)

        self._games = games
        self.SetBackgroundColour(wx.BLACK)
        self.SetItemCount(len(games))

        self._runningIdx = -1

    def _OnActivate(self, evt):
        self.Activate()
        evt.Skip()

    def _OnSelect(self, evt):
        wx.PostEvent(self, GameSelectEvent(game=self._games[evt.GetInt()]))
        evt.Skip()

    def SelectNext(self):
        next = self.GetSelection() + 1
        if next < self.GetItemCount():
            self.SetSelection(next)

    def SelectPrev(self):
        prev = self.GetSelection() - 1
        if prev >= 0:
            self.SetSelection(prev)

    def SetSelection(self, sel):
        wx.VListBox.SetSelection(self, sel)
        wx.PostEvent(self, GameSelectEvent(game=self._games[sel]))

    def Activate(self):
        sel = self.GetSelection()
        if sel == self._runningIdx:
            return

        if self._runningIdx != -1:
            wx.PostEvent(self, GameStopEvent(game=self._games[self._runningIdx]))

        self._runningIdx = sel

        wx.PostEvent(self, GameStartEvent(game=self._games[self._runningIdx]))

        self.Refresh()

    def OnDrawItem(self, dc, rect, n):
        font = self.GetFont()
        font.SetPointSize(12)

        if self.GetSelection() == n:
            c = wx.WHITE
            font.SetWeight(wx.FONTWEIGHT_BOLD)
        else:
            c = wx.Colour(200, 200, 200)

        dc.SetFont(font)

        dc.SetTextForeground(c)
        dc.DrawLabel(self._games[n].GetName(), rect,
                     wx.ALIGN_CENTER | wx.ALIGN_CENTER_VERTICAL)

    def OnDrawBackground(self, dc, rect, n):
        dc.SetPen(wx.Pen(wx.BLACK))
        dc.SetBrush(wx.Brush(wx.BLACK))

        dc.DrawRectangle(rect)

        if n in (self.GetSelection(), self._runningIdx):
            if n == self._runningIdx:
                if n == self.GetSelection():
                    cg1 = ColourGradient(wx.Colour(0, 0, 0), wx.Colour(0, 100, 0), rect.width // 2 + 1)
                    cg2 = ColourGradient(wx.Colour(0, 0, 0), wx.Colour(0, 255, 0), rect.width // 2 + 1)
                else:
                    cg1 = ColourGradient(wx.Colour(0, 0, 0), wx.Colour(0, 50, 0), rect.width // 2 + 1)
                    cg2 = ColourGradient(wx.Colour(0, 0, 0), wx.Colour(0, 128, 0), rect.width // 2 + 1)
            else:
              cg1 = ColourGradient(wx.Colour(0, 0, 0), wx.Colour(0, 0, 100), rect.width // 2 + 1)
              cg2 = ColourGradient(wx.Colour(0, 0, 0), wx.Colour(0, 0, 255), rect.width // 2 + 1)

            gc = wx.GraphicsContext.Create(dc)
            gc.SetAntialiasMode(False)

            for x, (colour1, colour2) in enumerate(zip(cg1, cg2)):
                gc.SetPen(wx.Pen(colour2))
                gc.StrokeLine(x,                  rect.y, x,                  rect.y + rect.height - 1)
                gc.StrokeLine(rect.width - x - 1, rect.y, rect.width - x - 1, rect.y + rect.height - 1)

                gc.SetPen(wx.Pen(colour1))
                gc.StrokeLine(x,                  rect.y + 1, x,                  rect.y + rect.height - 2)
                gc.StrokeLine(rect.width - x - 1, rect.y + 1, rect.width - x - 1, rect.y + rect.height - 2)

    # This method must be overridden.  It should return the height
    # required to draw the n'th item.
    def OnMeasureItem(self, n):
        return 30
