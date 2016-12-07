
import wx
import wx.richtext as rt
import wx.lib.agw.aui as aui

import mtx
from gui.WxRenderer import WxRenderer
from gui.ctrls.GameListBox import GameListBox, EVT_GAME_SELECT, EVT_GAME_START, EVT_GAME_STOP


class FrmMain(wx.Frame):

    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE, name=wx.FrameNameStr, gameConsole=None, games=None):
        wx.Frame.__init__(self, parent, id, title, pos, size, style, name)
        self.Bind(wx.EVT_CLOSE, self._OnClose)
        self.Bind(wx.EVT_CHAR_HOOK, self._OnKeyDown)

        self._gameConsole = gameConsole
        self._games = games
        self._curGame = None

        self._init_ctrls(parent, games)

        self._timer = wx.Timer(self)
        self._timer.Start(20)
        self.Bind(wx.EVT_TIMER, self._OnTimer, self._timer)

        self.SetSize(wx.Size(300, 300))
        self.SetSize(wx.Size(720, 600))

        self.SetTitle("Matrix Games - Game Console")
        self.SetIcons(self.GetFrameMainIconBundle())

        self.CenterOnScreen()

    @staticmethod
    def GetFrameMainIconBundle():
        ib = wx.IconBundle()
        ib.AddIcon(wx.ArtProvider.GetIcon('logo_16'))
        ib.AddIcon(wx.ArtProvider.GetIcon('logo_32'))
        ib.AddIcon(wx.ArtProvider.GetIcon('logo_48'))
        ib.AddIcon(wx.ArtProvider.GetIcon('logo_64'))
        return ib

    def _init_ctrls(self, parent, games):
        self.SetBackgroundColour(wx.BLACK)

        self._pnlField = wx.Panel(self)
        self._gameConsole.RegisterRenderer(WxRenderer(self._pnlField))

        self._lbGames = GameListBox(self, games=games)
        self._lbGames.Bind(EVT_GAME_SELECT, self._OnGameSelect)
        self._lbGames.Bind(EVT_GAME_START, self._OnGameStart)
        self._lbGames.Bind(EVT_GAME_STOP, self._OnGameStop)
        self._lbGames.SetSelection(0)
        self._lbGames.SetFocus()

        self._rtGameInfo = rt.RichTextCtrl(self, style=wx.VSCROLL | wx.NO_BORDER | rt.RE_READONLY)
        self._rtGameInfo.SetBackgroundColour(wx.BLACK)
        self._rtGameInfo.Disable()

        self._auiMgr = aui.AuiManager(self)
        self._auiMgr.SetAGWFlags(self._auiMgr.GetAGWFlags() |
                                 aui.AUI_MGR_TRANSPARENT_DRAG |
                                 aui.AUI_MGR_ALLOW_ACTIVE_PANE |
                                 aui.AUI_MGR_LIVE_RESIZE)

        ap = self._auiMgr.GetArtProvider()
        ap.SetMetric(aui.AUI_DOCKART_SASH_SIZE, 2)
        ap.SetColor(aui.AUI_DOCKART_BACKGROUND_COLOUR, wx.BLACK)
        ap.SetColor(aui.AUI_DOCKART_SASH_COLOUR, wx.Colour(20, 30, 40))

        self._auiMgr.AddPane(self._pnlField,
                             aui.AuiPaneInfo().Name('field').
                                                    CenterPane().
                                                    PaneBorder(False))

        self._auiMgr.AddPane(self._lbGames,
                             aui.AuiPaneInfo().Name('games').
                                                    Left().
                                                    Layer(0).
                                                    CaptionVisible(False).
                                                    MinSize(wx.Size(150, -1)).
                                                    Floatable(False).
                                                    MaximizeButton(False).
                                                    CloseButton(False).
                                                    PaneBorder(False))

        self._auiMgr.AddPane(self._rtGameInfo,
                             aui.AuiPaneInfo().Name('gameInfo').
                                                    Left().
                                                    Layer(0).
                                                    CaptionVisible(False).
                                                    Floatable(False).
                                                    MaximizeButton(False).
                                                    CloseButton(False).
                                                    PaneBorder(False))

        self._auiMgr.GetPane("games").dock_proportion = 100
        self._auiMgr.GetPane("gameInfo").dock_proportion = 150

        self._auiMgr.Update()

    def _OnGameSelect(self, evt):
        game = evt.game

        self._rtGameInfo.Clear()
        self._rtGameInfo.BeginTextColour(wx.WHITE)
        self._rtGameInfo.BeginBold()
        self._rtGameInfo.WriteText("Author")
        self._rtGameInfo.EndBold()
        self._rtGameInfo.EndTextColour()

        self._rtGameInfo.Newline()

        self._rtGameInfo.BeginLeftIndent(40)
        self._rtGameInfo.BeginTextColour(wx.Colour(200, 200, 200))
        self._rtGameInfo.WriteText(game.GetAuthor())
        self._rtGameInfo.Newline()
        self._rtGameInfo.EndTextColour()
        self._rtGameInfo.EndLeftIndent()

        self._rtGameInfo.Newline()

        self._rtGameInfo.BeginTextColour(wx.WHITE)
        self._rtGameInfo.BeginBold()
        self._rtGameInfo.WriteText("Max. Players")
        self._rtGameInfo.EndBold()
        self._rtGameInfo.EndTextColour()

        self._rtGameInfo.Newline()

        self._rtGameInfo.BeginLeftIndent(40)
        self._rtGameInfo.BeginTextColour(wx.Colour(200, 200, 200))
        self._rtGameInfo.WriteText(str(game.GetMaxPlayers()))
        self._rtGameInfo.Newline()
        self._rtGameInfo.EndTextColour()
        self._rtGameInfo.EndLeftIndent()

        self._rtGameInfo.Newline()

        self._rtGameInfo.BeginTextColour(wx.WHITE)
        self._rtGameInfo.BeginBold()
        self._rtGameInfo.WriteText("Description")
        self._rtGameInfo.EndBold()
        self._rtGameInfo.EndTextColour()

        self._rtGameInfo.Newline()

        self._rtGameInfo.BeginLeftIndent(40)
        self._rtGameInfo.BeginTextColour(wx.Colour(200, 200, 200))
        self._rtGameInfo.WriteText(game.GetDescription())
        self._rtGameInfo.Newline()
        self._rtGameInfo.EndTextColour()
        self._rtGameInfo.EndLeftIndent()

    def _OnGameStart(self, evt):
        self.StartGame(evt.game)

    def _OnGameStop(self, evt):
        self.StopGame()

    def StartGame(self, game):
        self._curGame = game()
        self._gameConsole.LoadGame(self._curGame)
        self._pnlField.SetFocus()

    def StopGame(self):
        self._curGame = None

    def _OnTimer(self, evt):
        self._gameConsole.Idle()
        evt.Skip()

    def _OnKeyDown(self, evt):
        keyCode = evt.GetKeyCode()

        if keyCode == wx.WXK_ESCAPE:
            if self._curGame is None:
                self.Close()
            else:
                self.StopGame()
        if keyCode == wx.WXK_RETURN:
            self._lbGames.Activate()
        elif keyCode == 85:
            self._gameConsole.Undo()
        elif keyCode == 82:
            self._gameConsole.ResetLevel()
        elif keyCode == wx.WXK_UP:
            if self._curGame is None:
                self._lbGames.SelectPrev()
            else:
                self._gameConsole.MovePlayer(1, mtx.UP)
        elif keyCode == wx.WXK_RIGHT:
            self._gameConsole.MovePlayer(1, mtx.RIGHT)
        elif keyCode == wx.WXK_DOWN:
            if self._curGame is None:
                self._lbGames.SelectNext()
            else:
                self._gameConsole.MovePlayer(1, mtx.DOWN)
        elif keyCode == wx.WXK_LEFT:
            self._gameConsole.MovePlayer(1, mtx.LEFT)
        elif keyCode == 87:
            self._gameConsole.JumpPlayer(1, mtx.UP)
        elif keyCode == 68:
            self._gameConsole.JumpPlayer(1, mtx.RIGHT)
        elif keyCode == 83:
            self._gameConsole.JumpPlayer(1, mtx.DOWN)
        elif keyCode == 65:
            self._gameConsole.JumpPlayer(1, mtx.LEFT)
        else:
            evt.Skip()

    def _OnClose(self, evt):
        self._timer.Stop()
        self._auiMgr.UnInit()
        evt.Skip()
