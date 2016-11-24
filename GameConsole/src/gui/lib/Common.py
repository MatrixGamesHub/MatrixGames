# -*- coding: ISO-8859-1 -*-

import wx
import math


class GraphicsContext(object):

    def __init__(self, dc, clippingRect=None):
        self._gc = wx.GraphicsContext.Create(dc)
        if clippingRect:
            self._gc.Clip(*clippingRect)

    def __enter__(self):
        return self._gc

    def __exit__(self, *args, **kwargs):
        del self._gc


class DCContextManager(object):
    def __init__(self, dc):
        self._dc = dc

    def __enter__(self):
        return self._dc

    def __exit__(self, *args, **kwargs):
        del self._dc


class ScreenDC(DCContextManager):

    def __init__(self):
        DCContextManager.__init__(self, wx.ScreenDC())


class MemoryDC(DCContextManager):

    def __init__(self, *args, **kwargs):
        DCContextManager.__init__(self, wx.MemoryDC(*args, **kwargs))


class ClientDC(DCContextManager):

    def __init__(self, *args, **kwargs):
        DCContextManager.__init__(self, wx.ClientDC(*args, **kwargs))


class BufferedPaintDC(DCContextManager):

    def __init__(self, *args, **kwargs):
        DCContextManager.__init__(self, wx.BufferedPaintDC(*args, **kwargs))


class ColourGradient(object):

    def __init__(self, startColour, endColour, size, includeEndColour=True):
        self._startColour = startColour.Get(True) if isinstance(startColour, wx.Colour) else startColour
        self._endColour = endColour.Get(True) if isinstance(endColour, wx.Colour) else endColour
        self._size = max(2, size)
        self._includeEndColour = includeEndColour
        if includeEndColour:
            self._size -= 1
        self._steps = [float((c2 - c1)) / self._size for c1, c2 in zip(self._startColour, self._endColour)]

    def __getitem__(self, idx):
        colour = list(self._startColour)
        for x in range(len(colour)):
              colour[x] += idx * self._steps[x]
        return wx.Colour(*colour)

    def __iter__(self):
        colour = list(self._startColour)
        yield wx.Colour(*colour)
        for step in range(self._size - 1):
            for x in range(len(colour)):
                colour[x] += self._steps[x]

            yield wx.Colour(*colour)

        if self._includeEndColour:
            yield wx.Colour(*self._endColour)


def Dc2GcRect(dcRect):
    return wx.Rect(dcRect.x, dcRect.y, dcRect.width - 1, dcRect.height - 1)


def DrawShadow(dc, rect, radius=0, size=5, colour=None, side=wx.RIGHT | wx.BOTTOM):

    rect = Dc2GcRect(rect)
    startColour = (0, 0, 0, 255) if colour is None else list(colour.Get(True))
    endColour = (0, 0, 0, 0) if colour is None else list(colour.Get()) + [0]

    with GraphicsContext(dc) as gc:
        gc.SetBrush(wx.TRANSPARENT_BRUSH)
        for d, colour in enumerate(ColourGradient(startColour, endColour, size, False)):
            started = False
            gc.SetPen(wx.Pen(colour))
            path = gc.CreatePath()

            x1 = rect.x
            y1 = rect.y
            x2 = x1 + rect.width
            y2 = y1 + rect.height
            r = radius

            if side & wx.LEFT:
                started = True
                path.MoveToPoint(x1 - 1 - d , y2 - r)
                path.AddLineToPoint(x1 - 1 - d, y1 + r)

            if side & wx.TOP:
                if started:
                    if r + d > 0:
                        path.AddArcToPoint(x1 - 1 - d, y1 - 1 - d , x1 + r, y1 - 1 - d, r + 1 + d)
                    else:
                        path.AddLineToPoint(x1 + r, y1 - 1 - d)
                else:
                    started = True
                    path.MoveToPoint(x1 + r, y1 - 1 - d)

                path.AddLineToPoint(x2 - r, y1 - 1 - d)
            else:
                started = False

            if side & wx.RIGHT:
                if started:
                    if r + d > 0:
                        path.AddArcToPoint(x2 + 1 + d, y1 - 1 - d, x2 + 1 + d, y1 + r, r + 1 + d)
                    else:
                        path.AddLineToPoint(x2 + 1 + d, y1 + r)
                else:
                    started = True
                    path.MoveToPoint(x2 + 1 + d, y1 + r)

                path.AddLineToPoint(x2 + 1 + d, y2 - r)
            else:
                started = False

            if side & wx.BOTTOM:
                if started:
                    if r + d > 0:
                        path.AddArcToPoint(x2 + 1 + d, y2 + 1 + d, x2 - r, y2 + 1 + d, r + 1 + d)
                    else:
                        path.AddLineToPoint(x2 - r, y2 + 1 + d)
                else:
                    started = True
                    path.MoveToPoint(x2 - r, y2 + 1 + d)

                path.AddLineToPoint(x1 + r, y2 + 1 + d)
            else:
                started = False

            if side & wx.LEFT:
                if started:
                    if r + d > 0:
                        path.AddArcToPoint(x1 - 1 - d, y2 + 1 + d, x1 - 1 - d, y2 - r, r + 1 + d)
                    else:
                       path.AddLineToPoint(x1 - 1 - d, y2 - r)

            gc.StrokePath(path)

            del path


def DrawRectangle(dc, rect, radius=0, dropShadow=False, shadowSize=5, shadowColour=None, shadowSides=wx.RIGHT | wx.BOTTOM):
    if dropShadow:
        DrawShadow(dc, rect, radius, shadowSize, shadowColour, shadowSides)
    rect = Dc2GcRect(rect)
    with GraphicsContext(dc) as gc:
        gc.SetPen(dc.GetPen())
        if rect.width == 0 or rect.height == 0:
            gc.StrokeLine(rect.x, rect.y, rect.x + rect.width, rect.y + rect.height)
        else:
            gc.SetBrush(dc.GetBrush())
            gc.DrawRoundedRectangle(*rect, radius=radius)
