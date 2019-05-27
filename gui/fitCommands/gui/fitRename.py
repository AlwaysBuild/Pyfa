import wx

import eos.db
import gui.mainFrame
from gui.builtinShipBrowser.events import FitRenamed
from gui.fitCommands.calc.fitRename import CalcFitRenameCommand
from gui.fitCommands.helpers import InternalCommandHistory


class GuiRenameFitCommand(wx.Command):

    def __init__(self, fitID, name):
        wx.Command.__init__(self, True, 'Rename Fit')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.name = name

    def Do(self):
        cmd = CalcFitRenameCommand(fitID=self.fitID, name=self.name)
        success = self.internalHistory.submit(cmd)
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), FitRenamed(fitID=self.fitID))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), FitRenamed(fitID=self.fitID))
        return success
