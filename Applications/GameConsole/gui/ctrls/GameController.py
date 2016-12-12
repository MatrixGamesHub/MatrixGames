
import wx
from gui.lib.Common import ColourGradient

GameSelectEvent, EVT_GAME_SELECT = wx.lib.newevent.NewEvent()
GameStartEvent, EVT_GAME_START = wx.lib.newevent.NewEvent()
GameStopEvent, EVT_GAME_STOP = wx.lib.newevent.NewEvent()


class GameController(wx.VListBox):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
                  name=wx.VListBoxNameStr, gameLoader=None):
        wx.VListBox.__init__(self, parent, id, pos, size, style | wx.NO_BORDER, name)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self._OnDClick)
        self.Bind(wx.EVT_LISTBOX, self._OnSelect)

        self._gameLoader = gameLoader
        self.SetBackgroundColour(wx.BLACK)

        self._runningIdx = -1

        self.Reload()

    def _OnDClick(self, evt):
        self.Start()
        evt.Skip()

    def _OnSelect(self, evt):
        self._PostGameEvent(GameSelectEvent, evt.GetInt())
        evt.Skip()

    def _PostGameEvent(self, evtClass, gameIdx):
        gameClass = self._gameLoader.GetGameClass(gameIdx)
        evt = evtClass(gameClass=gameClass, gameName=gameClass.GetName())
        wx.PostEvent(self, evt)

    def Reload(self):
        sel = self.GetSelection()
        runningIdx = self._runningIdx
        self.Stop()
        self._gameLoader.Load()
        self.SetItemCount(self._gameLoader.GetGamesCount())

        if sel < self._gameLoader.GetGamesCount():
            self.SetSelection(sel)

        if runningIdx < self._gameLoader.GetGamesCount():
            self.Start(runningIdx)

        self.Refresh()

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
        self._PostGameEvent(GameSelectEvent, sel)

    def Start(self, idx=None):
        if idx is None:
            idx = self.GetSelection()

        if idx == self._runningIdx:
            return

        if self._runningIdx != -1:
            self._PostGameEvent(GameStopEvent, self._runningIdx)

        self._runningIdx = idx
        self._PostGameEvent(GameStartEvent, self._runningIdx)

        self.Refresh()

    def Stop(self):
        if self._runningIdx != -1:
            self._PostGameEvent(GameStopEvent, self._runningIdx)
            self._runningIdx = -1
            self.Refresh()

    def OnDrawItem(self, dc, rect, idx):
        font = self.GetFont()
        font.SetPointSize(12)

        if self.GetSelection() == idx:
            c = wx.WHITE
            font.SetWeight(wx.FONTWEIGHT_BOLD)
        else:
            c = wx.Colour(200, 200, 200)

        dc.SetFont(font)

        dc.SetTextForeground(c)
        dc.DrawLabel(self._gameLoader.GetGameName(idx), rect,
                     wx.ALIGN_CENTER | wx.ALIGN_CENTER_VERTICAL)

    def OnDrawBackground(self, dc, rect, idx):
        dc.SetPen(wx.Pen(wx.BLACK))
        dc.SetBrush(wx.Brush(wx.BLACK))

        dc.DrawRectangle(rect)

        if idx in (self.GetSelection(), self._runningIdx):
            if idx == self._runningIdx:
                if idx == self.GetSelection():
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
    def OnMeasureItem(self, idx):
        return 30
