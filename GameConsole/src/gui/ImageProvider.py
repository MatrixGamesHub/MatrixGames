import wx

from wx.lib.art import img2pyartprov
import res.Images


class ImageProvider(object):

    provider = None

    @classmethod
    def Init(cls):
        if cls.provider is None:
            cls.provider = img2pyartprov.Img2PyArtProvider(res.Images, artIdPrefix='')
            wx.ArtProvider.Push(cls.provider)
