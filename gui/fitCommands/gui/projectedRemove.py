import math

import wx

import eos.db
import gui.mainFrame
from eos.saveddata.drone import Drone as EosDrone
from eos.saveddata.fighter import Fighter as EosFighter
from eos.saveddata.fit import Fit as EosFit
from eos.saveddata.module import Module as EosModule
from gui import globalEvents as GE
from gui.fitCommands.calc.drone.projectedRemove import CalcRemoveProjectedDroneCommand
from gui.fitCommands.calc.fighter.projectedRemove import CalcRemoveProjectedFighterCommand
from gui.fitCommands.calc.module.projectedRemove import CalcRemoveProjectedModuleCommand
from gui.fitCommands.calc.projectedFit.remove import CalcRemoveProjectedFitCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiRemoveProjectedItemsCommand(wx.Command):

    def __init__(self, fitID, items, amount):
        wx.Command.__init__(self, True, 'Remove Projected Items')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.amount = amount
        self.pModPositions = []
        self.pDroneItemIDs = []
        self.pFighterPositions = []
        self.pFitIDs = []
        fit = Fit.getInstance().getFit(fitID)
        for item in items:
            if isinstance(item, EosModule):
                if item in fit.projectedModules:
                    self.pModPositions.append(fit.projectedModules.index(item))
            elif isinstance(item, EosDrone):
                self.pDroneItemIDs.append(item.itemID)
            elif isinstance(item, EosFighter):
                if item in fit.projectedFighters:
                    self.pFighterPositions.append(fit.projectedFighters.index(item))
            elif isinstance(item, EosFit):
                self.pFitIDs.append(item.ID)

    def Do(self):
        results = []
        for pModPosition in sorted(self.pModPositions, reverse=True):
            cmd = CalcRemoveProjectedModuleCommand(fitID=self.fitID, position=pModPosition, commit=False)
            results.append(self.internalHistory.submit(cmd))
        for pDroneItemID in self.pDroneItemIDs:
            cmd = CalcRemoveProjectedDroneCommand(fitID=self.fitID, itemID=pDroneItemID, amount=self.amount, commit=False)
            results.append(self.internalHistory.submit(cmd))
        for pFighterPosition in sorted(self.pFighterPositions, reverse=True):
            cmd = CalcRemoveProjectedFighterCommand(fitID=self.fitID, position=pFighterPosition, commit=False)
            results.append(self.internalHistory.submit(cmd))
        for pFitID in self.pFitIDs:
            cmd = CalcRemoveProjectedFitCommand(fitID=self.fitID, projectedFitID=pFitID, amount=self.amount, commit=False)
            results.append(self.internalHistory.submit(cmd))
        success = any(results)
        eos.db.commit()
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        eos.db.commit()
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
