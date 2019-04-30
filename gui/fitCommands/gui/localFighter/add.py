import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.fighter.localAdd import CalcAddLocalFighterCommand
from gui.fitCommands.helpers import FighterInfo, InternalCommandHistory
from service.fit import Fit


class GuiAddLocalFighterCommand(wx.Command):

    def __init__(self, fitID, itemID):
        wx.Command.__init__(self, True, 'Add Local Fighter')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.itemID = itemID

    def Do(self):
        cmd = CalcAddLocalFighterCommand(fitID=self.fitID, fighterInfo=FighterInfo(itemID=self.itemID))
        success = self.internalHistory.submit(cmd)
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
