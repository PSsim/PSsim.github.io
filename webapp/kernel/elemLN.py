import numpy as np
import scipy.sparse as sp

# (Line.con) 1 from, 2 to, 3 SB, 4 VB, 5 FB, 6 length, 7 prim/seq volt, 8 R/km, 9 X/km, 10 B/km, 11 tap ratio, 12 phase shift, 13 Imax, 14 Pmax, 15 Smax(series comp.), 16 u


def fcn_LN_setup(self, Bus):
    ############################################################
    self.CompleteColumn(16)
    # ------------------------
    # apply series compensation to line impedances for power flow calculation
    self.con[:, 9-1] = (1-self.con[:, 15-1])*self.con[:, 9-1]
    # ------------------------
    self.n = self.con.shape[0]
    self.u = self.con[:, 16-1]
    # ------------------------
    # if tap ratio is zero it is set to one
    self.con[self.con[:, 11-1] == 0, 11-1] = 1
    # ------------------------
    # define Bus data using what was entered in Line data
    Bus.con = np.unique(self.con[:, :2].reshape(2*self.n, 1)).reshape(-1, 1)
    ############################################################
    return self, Bus


def fcn_LN_build_y(self, Shunt, N):
    ############################################################
    # line data and admittance matrix calculation
    RBranch = self.con[:, 8-1]
    XBranch = self.con[:, 9-1]
    BLine = self.con[:, 10-1]/2
    TapRatio = self.con[:, 11-1]
    angle = self.con[:, 12-1]*np.pi/180
    m = TapRatio*np.exp(1j*angle)
    # ------------------------
    selfYli = self.u/(RBranch + 1j*XBranch)
    selfYb2 = self.u*1j*BLine
    # ------------------------
    line_fr_fr = selfYli/TapRatio**2+selfYb2
    line_to_to = selfYli+selfYb2
    line_to_fr = -selfYli/m
    line_fr_to = -selfYli/np.conj(m)
    # ------------------------
    self.Y = sp.csr_matrix((line_fr_fr, (self.fr, self.fr)), shape=(N, N))
    self.Y += sp.csr_matrix((line_to_to, (self.to, self.to)), shape=(N, N))
    self.Y += sp.csr_matrix((line_to_fr, (self.to, self.fr)), shape=(N, N))
    self.Y += sp.csr_matrix((line_fr_to, (self.fr, self.to)), shape=(N, N))
    # ------------------------
    # shunt data and admittance matrix update
    if Shunt.n != 0:
        GShunt = Shunt.con[:, 5-1]
        BShunt = Shunt.con[:, 6-1]
        shunt_bus = GShunt + 1j*BShunt
        self.Y += sp.csr_matrix((shunt_bus, (Shunt.bus,
                                Shunt.bus)), shape=(N, N))
    ############################################################
    return self
