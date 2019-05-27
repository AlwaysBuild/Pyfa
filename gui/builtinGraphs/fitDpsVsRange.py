# =============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
# =============================================================================


from collections import OrderedDict

from eos.graph.fitDpsVsRange import FitDpsVsRangeGraph as EosGraph
from gui.graph import Graph, XDef, YDef, ExtraInput


class FitDpsVsRangeGraph(Graph):

    name = 'DPS vs Range'

    def __init__(self):
        super().__init__()
        self.eosGraph = EosGraph()

    @property
    def xDef(self):
        return XDef(inputDefault='0-100', inputLabel='Distance to target (km)', inputIconID=1391, axisLabel='Distance to target, km')

    @property
    def yDefs(self):
        return OrderedDict([('dps', YDef(switchLabel='DPS', axisLabel='DPS', eosGraph='eosGraph'))])

    @property
    def extraInputs(self):
        return OrderedDict([
            ('speed', ExtraInput(inputDefault=0, inputLabel='Target speed (m/s)', inputIconID=1389)),
            ('signatureRadius', ExtraInput(inputDefault=None, inputLabel='Target signature radius (m)', inputIconID=1390)),
            ('angle', ExtraInput(inputDefault=0, inputLabel='Target angle (degrees)', inputIconID=1389))])

    @property
    def hasTargets(self):
        return True

    @property
    def hasVectors(self):
        return True


FitDpsVsRangeGraph.register()
