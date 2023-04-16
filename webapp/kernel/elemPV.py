import numpy as np

# (PV.con) 1 Bus, 2 SB, 3 VB, 4 Pg, 5 V0, 6 Qmax, 7 Qmin, 8 Vmax, 9 Vmin, 10 Loss part, 11 u


def fcn_PV_setup(self, Bus, SW):
    ############################################################
    self.CompleteColumn(11)
    # ------------------------
    self = fcn_PVremove(self, SW)
    # ------------------------
    self.BusesIdx(Bus)
    ############################################################
    return self


def fcn_PV_base(self, Bus, SBASE):
    ############################################################
    SBold = self.con[:, 2-1]
    SBnew = SBASE
    # ------------------------
    VBold = self.con[:, 3-1]
    VBnew = Bus.con[self.bus, 2-1]  # voltage base of I bus
    # ------------------------
    #
    # ------------------------
    # Powers are converted to the system base
    self.con[:, 4-1] = self.con[:, 4-1] * SBold/SBnew
    self.con[:, 6-1] = self.con[:, 6-1] * SBold/SBnew
    self.con[:, 7-1] = self.con[:, 7-1] * SBold/SBnew
    # ------------------------
    self.con[:, 8-1] = self.con[:, 8-1] * VBold/VBnew
    self.con[:, 9-1] = self.con[:, 9-1] * VBold/VBnew
    ############################################################
    return self


def fcn_PVremove(self, SW):
    ############################################################
    # remove PV buses listed as SW buses
    buses_SW = set(SW.con[:, 0])
    buses_PV = set(self.con[:, 0])
    # ------------------------
    buses_intersec = buses_PV & buses_SW    # intersection
    A = np.array(list(buses_intersec))
    idx = np.where(np.isin(self.con[:, 0], A))
    self.con = np.delete(self.con, idx, axis=0)
    ############################################################
    return self
