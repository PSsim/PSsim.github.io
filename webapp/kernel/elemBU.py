import numpy as np


def fcn_BU_setup(self, Line):
    ############################################################
    self.n = self.con.shape[0]
    self.a = np.arange(self.n)
    self.v = self.a + self.n
    # ------------------------
    # if not defined, complete with base voltage equal to one
    if self.con.shape[1] == 1:
        self.con = np.concatenate((self.con, np.ones((self.n, 1))), axis=1)
    # ------------------------
    # internal bus numbers for second indexing of buses
    self.int = np.arange(self.con[:, 0].max()).astype(int)*0-1
    idx_int = (self.con[:, 0]-1).astype(int)
    self.int[idx_int] = self.a
    # ------------------------
    # indexing for line buses
    idx_int = (Line.con[:, 0]-1).astype(int)
    Line.fr = self.int[idx_int]
    idx_int = (Line.con[:, 1]-1).astype(int)
    Line.to = self.int[idx_int]
    ############################################################
    return self, Line
