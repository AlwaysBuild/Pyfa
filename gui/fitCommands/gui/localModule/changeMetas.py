import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.module.localReplace import CalcReplaceLocalModuleCommand
from gui.fitCommands.helpers import InternalCommandHistory, ModuleInfo, restoreRemovedDummies
from service.fit import Fit


class GuiChangeLocalModuleMetasCommand(wx.Command):

    def __init__(self, fitID, positions, newItemID):
        wx.Command.__init__(self, True, 'Change Local Module Metas')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.positions = positions
        self.newItemID = newItemID
        self.relacedItemIDs = None
        self.savedRemovedDummies = None

    def Do(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        commands = []
        self.replacedItemIDs = set()
        for position in self.positions:
            module = fit.modules[position]
            if module.isEmpty:
                continue
            if module.itemID == self.newItemID:
                continue
            self.replacedItemIDs.add(module.itemID)
            info = ModuleInfo.fromModule(module)
            info.itemID = self.newItemID
            cmd = CalcReplaceLocalModuleCommand(
                fitID=self.fitID,
                position=position,
                newModInfo=info,
                unloadInvalidCharges=True)
            commands.append(cmd)
        if not commands:
            return False
        success = self.internalHistory.submitBatch(*commands)
        eos.db.flush()
        sFit.recalc(self.fitID)
        self.savedRemovedDummies = sFit.fill(self.fitID)
        eos.db.commit()
        events = []
        if success and self.replacedItemIDs:
            events.append(GE.FitChanged(fitID=self.fitID, action='moddel', typeID=self.replacedItemIDs))
        if success:
            events.append(GE.FitChanged(fitID=self.fitID, action='modadd', typeID=self.newItemID))
        if not events:
            events.append(GE.FitChanged(fitID=self.fitID))
        for event in events:
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), event)
        return success

    def Undo(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        restoreRemovedDummies(fit, self.savedRemovedDummies)
        success = self.internalHistory.undoAll()
        eos.db.flush()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        eos.db.commit()
        events = []
        if success:
            events.append(GE.FitChanged(fitID=self.fitID, action='moddel', typeID=self.newItemID))
        if success and self.replacedItemIDs:
            events.append(GE.FitChanged(fitID=self.fitID, action='modadd', typeID=self.replacedItemIDs))
        if not events:
            events.append(GE.FitChanged(fitID=self.fitID))
        for event in events:
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), event)
        return success
