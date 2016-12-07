
import wx
import os
import sys

distPath = 'dist' if len(sys.argv) == 1 else sys.argv[1]

app = wx.App()


def CreateLogo(size):
    logo = ['-######',
            '-#1B  #',
            '### # #',
            '#  bt #',
            '# # ###',
            '#   #--',
            '#####--']

    bmp = wx.Bitmap(size, size)

    pixelSize = size // 7
    padding = 2 if size <= 64 else 3
    margin = (size - (pixelSize * 7) + padding - 1) // 2
    radius = 0 if size <= 64 else 1
    dcBmp = wx.MemoryDC(bmp)

    if size == 16:
        alpha = 160
    elif size == 32:
        alpha = 80
    elif size == 48:
        alpha = 60
    else:
        alpha = 60

    for y, row in enumerate(logo):
        for x, sign in enumerate(row):
            if sign == '#':
                colour = wx.RED
            elif sign == '1':
                colour = wx.Colour(0, 153, 255)
            elif sign == 'B':
                colour = wx.GREEN
            elif sign == 'b':
                 colour = wx.Colour(226, 209, 29)
            elif sign == 't':
                colour = wx.Colour(161, 161, 161)
            elif sign == ' ':
                colour = wx.WHITE
            elif sign == '-':
                continue

            gc = wx.GraphicsContext.Create(dcBmp)
            gc.SetBrush(wx.Brush(colour=colour))
            gc.SetPen(wx.Pen(colour=colour))

            path = gc.CreatePath()

            # Draw the Pixel
            if pixelSize - padding <= 1:
                pixel = wx.Bitmap(1, 1)
                dcPixel = wx.MemoryDC(pixel)
                dcPixel.SetBackground(wx.Brush(colour=colour))
                dcPixel.Clear()
                del dcPixel

                gc.DrawBitmap(pixel, margin + x * pixelSize, margin + y * pixelSize, 1, 1)

                path.MoveToPoint(margin + x * pixelSize, margin + (y + 1) * pixelSize - 1)
                path.AddLineToPoint(margin + (x + 1) * pixelSize - 1, margin + (y + 1) * pixelSize - 1)
                path.AddLineToPoint(margin + (x + 1) * pixelSize - 1, margin + y * pixelSize)


            else:
                gc.DrawRoundedRectangle(margin + x * pixelSize,
                                        margin + y * pixelSize,
                                        pixelSize - padding,
                                        pixelSize - padding, radius)

                delta = radius if radius > 0 else 1
                path.MoveToPoint(margin + (x + 1) * pixelSize - padding + 1, margin + y * pixelSize + delta)
                if radius > 0:
                    path.AddLineToPoint(margin + (x + 1) * pixelSize - padding + 1,
                                        margin + (y + 1) * pixelSize - padding + 1 - radius)

                    path.AddArcToPoint( margin + (x + 1) * pixelSize - padding + 1,
                                        margin + (y + 1) * pixelSize - padding + 1,
                                        margin + (x + 1) * pixelSize - padding + 1 - radius,
                                        margin + (y + 1) * pixelSize - padding + 1,
                                        radius
                                        )
                    path.AddLineToPoint(margin + x * pixelSize + delta, margin + (y + 1) * pixelSize - padding + 1)
                else:
                    gc.SetAntialiasMode(wx.ANTIALIAS_NONE)
                    path.AddLineToPoint(margin + (x + 1) * pixelSize - padding + 1, margin + (y + 1) * pixelSize - padding + 1)
                    path.AddLineToPoint(margin + x * pixelSize + delta, margin + (y + 1) * pixelSize - padding + 1)

            gc.SetPen(wx.Pen(colour=wx.Colour(colour.red, colour.green, colour.blue, alpha)))
            gc.StrokePath(path)
            del path

            del gc

    del dcBmp

    bmp.SaveFile('{0}/logo_{1:03d}x{1:03d}.png'.format(distPath, size), wx.BITMAP_TYPE_PNG)

if not os.path.isdir(distPath):
    os.mkdir(distPath)

for size in (16, 32, 48, 64, 128, 256, 512):
    CreateLogo(size)
