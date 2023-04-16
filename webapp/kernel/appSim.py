import numpy as np
from kernel.elemBU import fcn_BU_setup
from kernel.elemLN import fcn_LN_setup, fcn_LN_build_y
from kernel.elemSH import fcn_SH_setup
from kernel.elemSW import fcn_SW_setup
from kernel.elemPV import fcn_PV_setup, fcn_PV_base
from kernel.elemPQ import fcn_PQ_setup
from kernel.appPF import fcn_NR


def fcn_Sim(dataLN_str, dataSH_str, dataSW_str, dataPV_str, dataPQ_str, Dims):
    ############################################################
    LNdata = np.fromstring(dataLN_str, sep=' ').reshape((Dims[0], -1))
    SHdata = np.fromstring(dataSH_str, sep=' ').reshape((Dims[1], -1))
    SWdata = np.fromstring(dataSW_str, sep=' ').reshape((Dims[2], -1))
    PVdata = np.fromstring(dataPV_str, sep=' ').reshape((Dims[3], -1))
    PQdata = np.fromstring(dataPQ_str, sep=' ').reshape((Dims[4], -1))
    # ------------------------

    class MyElements:
        def __init__(self):
            self.con = []
            self.n = 0

        def BusesIdx(self, Bus):        # Method of MyElements
            if isinstance(self.con, np.ndarray):
                self.n = self.con.shape[0]
                idx_int = (self.con[:, 0]-1).astype(int)
                self.bus = Bus.int[idx_int]
                self.vbus = self.bus + Bus.n

        def CompleteColumn(self, ncol):  # Method of MyElements
            columns = self.con.shape[1]
            if columns < ncol:
                self.con = np.concatenate(
                    (self.con, np.zeros((self.con.shape[0], ncol-columns))), axis=1)
                self.con[:, ncol-1] = 1

    # ------------------------
    Bus = MyElements()
    Line = MyElements()
    Shunt = MyElements()
    SW = MyElements()
    PV = MyElements()
    PQ = MyElements()
    # ------------------------
    Line.con = LNdata
    if SHdata[0, 0] != 0:
        Shunt.con = SHdata
    SW.con = SWdata
    PV.con = PVdata
    PQ.con = PQdata
    # ------------------------
    SBASE = 100
    # ------------------------
    Line, Bus = fcn_LN_setup(Line, Bus)
    Bus, Line = fcn_BU_setup(Bus, Line)
    Shunt = fcn_SH_setup(Shunt, Bus)
    SW = fcn_SW_setup(SW, Bus)
    PV = fcn_PV_setup(PV, Bus, SW)
    PQ = fcn_PQ_setup(PQ, Bus, SW, PV, SBASE)
    # ------------------------
    PV = fcn_PV_base(PV, Bus, SBASE)
    # ------------------------
    Line = fcn_LN_build_y(Line, Shunt, Bus.n)
    # ------------------------
    # flat initial guess
    seedSW = np.zeros(SW.n)
    seedPV = np.ones(PV.n)
    seedPQ = np.ones(PQ.n)
    th0 = SW.con[0, 5-1]
    x0 = np.concatenate(
        (seedSW, seedSW, 0*seedPV, th0*seedPV, th0*seedPQ, seedPQ))
    # ------------------------
    FLAG, Mx = fcn_NR(x0, SW, PV, PQ, Bus, Line)
    ############################################################
    return FLAG, Mx, Bus, SW, PV, PQ, Line
