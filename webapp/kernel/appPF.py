import numpy as np
import scipy.sparse as sp


def fcn_NR(x, SW, PV, PQ, Bus, Line):
    ############################################################
    MAXIT = 100   # maximum number of iterations

    Mx = np.zeros((4*Bus.n, MAXIT))  # Mx size is pre-defined

    for it in range(1, MAXIT+1):
        # ------------------------
        Bus = fcn_x2bus(x, SW, PV, PQ, Bus)
        # ------------------------
        # save data of this iteration
        Mx[:, it-1] = np.concatenate((Bus.ph, Bus.qh, Bus.vh, Bus.ah))
        # ------------------------
        f = fcn_f(Bus, Line.Y)
        jac = fcn_jac(SW, PV, PQ, Bus, Line.Y)
        Dx = -sp.linalg.spsolve(jac, f)  # -inv(jac)*f
        x = x + Dx
        # ------------------------
        aux = np.abs(Dx)
        if aux.max() < 1e-7:
            FLAG = "Convergence in " + str(it) + " iterations"
            break
    if it == MAXIT:
        FLAG = "Did not converge."
    else:
        Bus = fcn_x2bus(x, SW, PV, PQ, Bus)
        # save data of the last iteration (final result)
        Mx[:, it] = np.concatenate((Bus.ph, Bus.qh, Bus.vh, Bus.ah))
        Mx = Mx[:, :it+1]  # remove the rest of the array Mx
    return FLAG, Mx
    ############################################################


def fcn_f(Bus, Y):
    ############################################################
    V = Bus.vh*np.exp(1j*Bus.ah)
    fcpx = (Bus.ph + 1j*Bus.qh) - V*np.conj(Y@V)
    return np.concatenate((np.real(fcpx), np.imag(fcpx)))
    ############################################################


def fcn_jac(SW, PV, PQ, Bus, Y):
    ############################################################
    thfp = Bus.ah
    Vmfp = Bus.vh
    # ------------------------
    expth = np.exp(1j*thfp)
    vn = Vmfp*expth
    # ------------------------
    U = sp.diags(expth, format='csr')
    V = sp.diags(vn, format='csr')
    Yc = np.conj(Y)
    diagIc = sp.diags(Yc@np.conj(vn), format='csr')
    # ------------------------
    dgdp = sp.identity(Bus.n, format='csr')
    dgdq = 1j*dgdp
    dgdth = -1j*V@(diagIc - Yc@np.conj(V))
    dgdva = -(U@diagIc + V@Yc@np.conj(U))
    # ------------------------
    dgdp = dgdp[:, SW.bus]
    dgdq = dgdq[:, np.concatenate((SW.bus, PV.bus))]
    dgdth = dgdth[:, np.concatenate((PV.bus, PQ.bus))]
    dgdva = dgdva[:, PQ.bus]
    # ------------------------
    dg = sp.hstack([dgdp, dgdq, dgdth, dgdva])
    # ------------------------
    Jac = sp.vstack([np.real(dg), np.imag(dg)])
    return Jac
    ############################################################


def fcn_x2bus(x, SW, PV, PQ, Bus):
    ############################################################
    Bus.ph = np.zeros(Bus.n)
    Bus.qh = np.zeros(Bus.n)
    Bus.ah = np.zeros(Bus.n)
    Bus.vh = np.zeros(Bus.n)
    # ------------------------
    # unknown variables
    Bus.ph[SW.bus] = x[: SW.n]
    Bus.qh[SW.bus] = x[SW.n: 2*SW.n]
    Bus.qh[PV.bus] = x[2*SW.n: 2*SW.n+PV.n]
    Bus.ah[PV.bus] = x[2*SW.n+PV.n: 2*SW.n+2*PV.n]
    Bus.ah[PQ.bus] = x[2*SW.n+2*PV.n: 2*SW.n+2*PV.n+PQ.n]
    Bus.vh[PQ.bus] = x[2*SW.n+2*PV.n+PQ.n: 2*SW.n+2*PV.n+2*PQ.n]
    # ------------------------
    # known variables
    Bus.vh[SW.bus] = SW.con[:, 4-1]
    Bus.ah[SW.bus] = SW.con[:, 5-1]
    Bus.vh[PV.bus] = PV.con[:, 5-1]
    Bus.ph[PV.bus] = PV.con[:, 4-1]
    Bus.ph[PQ.bus] = PQ.con[:, 4-1]
    Bus.qh[PQ.bus] = PQ.con[:, 5-1]
    return Bus
    ############################################################
