
import wx
import mtx


class WxRenderer(mtx.Renderer):

    def __init__(self, window):
        self._window = window
        self._level = None
        self._bmp = None
        self._dcBmp = None
        self._pixelSize = None
        self._margin = wx.Point(10, 10)
        self._padding = wx.Point(0, 0)
        self._bgColour = wx.BLACK

        window.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)

        self._window.Bind(wx.EVT_PAINT, self._OnPaint)
        self._window.Bind(wx.EVT_SIZE, self._OnSize)

    def ProcessActGroup(self, actGrp):
        for act in actGrp:
            if act.id == mtx.Act.CLEAR:
                self._level = None
                self._InitBitmap()

            if act.id in mtx.Act.LEVEL:
                self._level = act.level
                self._InitBitmap()
                self._DrawBitmap()

            if act.id == mtx.Act.SPAWN:
                field = self._level.GetField()
                cell = field.GetCell(act.position)
                self._DrawCell(cell)

            if act.id in mtx.Act.MOTION:
                field = self._level.GetField()
                fromCell = field.GetCell(act.fromX, act.fromY)
                if fromCell is not None:
                    self._DrawCell(fromCell)

                toCell = field.GetCell(act.toX, act.toY)
                if toCell is not None:
                    self._DrawCell(toCell)

        self._window.Refresh()

    def _OnPaint(self, evt):
        if self._dcBmp is None:
            return

        dc = wx.PaintDC(self._window)
        try:
            dc.Blit(0, 0, self._bmp.GetWidth(), self._bmp.GetHeight(),
                self._dcBmp, 0, 0, wx.COPY, False)
        finally:
            del dc
            evt.Skip()

    def _OnSize(self, evt):
        self._InitBitmap()
        self._DrawBitmap()
        self._window.Refresh()
        evt.Skip()

    def _InitBitmap(self):
        width, height = self._window.GetClientSize()

        self._bmp = wx.Bitmap(width, height)
        self._dcBmp = wx.MemoryDC(self._bmp)
        self._dcBmp.SetBackground(wx.Brush(colour=self._bgColour))
        self._dcBmp.Clear()

        width -= 2 * self._margin.x
        height -= 2 * self._margin.y

        if self._level is None:
            self._pixelSize = None
            self._padding = wx.Point(0, 0)
        else:
            fWidth, fHeight = self._level.GetField().GetSize()

            self._pixelSize = min(width // fWidth, height // fHeight)
            self._padding = wx.Point(max(0, (width - (self._pixelSize * fWidth)) // 2),
                                     max(0, (height - (self._pixelSize * fHeight)) // 2))

    def _DrawPixel(self, x, y, colour):
        # Clear pixel first, to avoid relicts on the edges from antialiasing.
        self._dcBmp.SetPen(wx.Pen(colour=self._bgColour))
        self._dcBmp.SetBrush(wx.Brush(colour=self._bgColour))
        self._dcBmp.DrawRectangle(self._margin.x + self._padding.x + x * self._pixelSize,
                                  self._margin.y + self._padding.y + y * self._pixelSize,
                                  self._pixelSize, self._pixelSize)

        # Use GraphicsContext for antialiasing
        gc = wx.GraphicsContext.Create(self._dcBmp)

        # Draw the Pixel
        gc.SetBrush(wx.Brush(colour=colour))
        gc.SetPen(wx.Pen(colour=colour))
        gc.DrawRoundedRectangle(self._margin.x + self._padding.x + x * self._pixelSize + 1,
                                self._margin.y + self._padding.y + y * self._pixelSize + 1,
                                self._pixelSize - 2, self._pixelSize - 2, 2)

        del gc

    def _DrawCell(self, cell):
        colour = wx.BLACK
        obj = cell.GetFirstObject()
        if obj is not None:
            if obj.GetSymbol() == '#':
                colour = wx.RED
            elif obj.GetSymbol() == '1':
                colour = wx.WHITE
            elif obj.GetSymbol() == 'b':
                if 't' in cell:
                    colour = wx.GREEN
                else:
                    colour = wx.YELLOW
            elif obj.GetSymbol() == 't':
                colour = wx.Colour(120,  55, 0)
            elif obj.GetSymbol() == '+':
                cnt = cell.GetObjectCount('+')
                if cnt == 1:
                    colour = wx.GREEN
                elif cnt == 2:
                    colour = wx.BLUE
                else:
                    colour = wx.RED
            elif obj.GetSymbol() == '.':
                colour = wx.YELLOW

        self._DrawPixel(cell._x, cell._y, colour)

    def _DrawBitmap(self):
        self._dcBmp.Clear()

        if self._level is None:
            return

        for cell in self._level.GetField():
            self._DrawCell(cell)
