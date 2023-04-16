import numpy as np

# (PQ.con) 1 Bus, 2 SB, 3 VB, 4 PL, 5 QL, 6 Vmax, 7 Vmin, 8 con to imped, 9 u


def fcn_PQ_setup(self, Bus, SW, PV, SB):
    ############################################################
    self.CompleteColumn(9)
    # ------------------------
    self = fcn_PQfill(Bus, SW, PV, self, SB)
    # ------------------------
    self.BusesIdx(Bus)
    # ------------------------
    # loads take power in power flow
    self.con[:, 3:5] = -self.con[:, 3:5]
    ############################################################
    return self


def fcn_PQfill(Bus, SW, PV, PQ, SB):
    ############################################################
    # fill PQ data with buses having zero consumption
    buses_BU = set(Bus.con[:, 0])
    buses_SW = set(SW.con[:, 0])
    buses_PV = set(PV.con[:, 0])
    buses_PQ = set(PQ.con[:, 0])
    # ------------------------
    buses_union = buses_SW | buses_PV | buses_PQ  # union
    # ------------------------
    buses_PQzero = buses_BU - buses_union  # difference
    # ------------------------
    A = np.array(list(buses_PQzero))
    idx = np.where(np.isin(Bus.con[:, 0], A))
    Vbase = Bus.con[idx, 1]  # voltage base
    # ------------------------
    PQzero = np.zeros((len(buses_PQzero), 9))
    PQzero[:, 0] = A
    PQzero[:, 1] = SB
    PQzero[:, 2] = Vbase
    PQzero[:, 9-1] = 1
    PQ.con = np.concatenate((PQ.con, PQzero))
    ############################################################
    return PQ
