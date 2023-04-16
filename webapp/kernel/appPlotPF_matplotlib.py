import numpy as np
import matplotlib.pyplot as plt


def fcn_Plot_VP(Bus, SW, PV, PQ):
    ############################################################
    Buses = np.arange(1, Bus.n+1)
    BusesName = Bus.con[:, 0]
    # ------------------------
    # fig, ax = plt.subplots(figsize=(10, 5), facecolor='none')
    fig, ax = plt.subplots()
    ax.set_title("voltage profile")
    ax.set_xlabel("buses")
    ax.set_ylabel("voltage [pu]")
    ax.axhline(y=1.05, color='red', linewidth=1, linestyle='--')
    ax.axhline(y=0.95, color='red', linewidth=1, linestyle='--')
    ax.plot(Buses, Bus.vh, color='black', linewidth=1.0, linestyle='-')
    ax.plot(Buses[PQ.bus], Bus.vh[PQ.bus], color='red',
            linestyle='none', marker='o', markersize=1.7, label='PQ bus')
    ax.plot(Buses[PV.bus], Bus.vh[PV.bus], color='blue',
            linestyle='none', marker='o', markersize=3, label='PV bus')
    ax.plot(Buses[SW.bus], Bus.vh[SW.bus], color='magenta',
            linestyle='none', marker='o', markersize=5, label='SW bus')
    fig.set_facecolor('none')
    # fig.subplots_adjust(right=0.8)  # Ajustar el espacio en blanco en el lado derecho del gráfico
    ax.legend()
    # ax.grid(True)
    # ax.set_axisbelow(True)
    ax.axis([1, Bus.n, 0.95*min(Bus.vh), 1.05*max(Bus.vh)])
    if Bus.n < 100:
        # plt.xticks(Buses, range(1, Bus.n+1), rotation=90)
        plt.xticks(Buses, BusesName.astype(int), rotation=90)
    # plt.close('all')
    # plt.close()
    ############################################################
    return fig


def fcn_Plot_VPC(Bus, SW, PV, PQ):
    ############################################################
    # Repetimos el primer elemento para que no se solape el primer y último valor, y arrancamos de 90º para que el primer valor arranque desde arriba.
    # BusesNameExt = np.concatenate([Bus.con[:, 0], [Bus.con[0, 0]]]).astype(int)
    radius = np.concatenate([Bus.vh, [Bus.vh[0]]])
    theta = np.linspace(5*np.pi/2, np.pi/2, Bus.n+1)
    x = radius*np.cos(theta)
    y = radius*np.sin(theta)
    # xTxT = 1.15*np.cos(theta)-0.07
    # yTxT = 1.15*np.sin(theta)-0.05
    # ------------------------
    # fig, ax = plt.subplots(figsize=(7, 7), layout='constrained', facecolor='none')
    fig, ax = plt.subplots()
    ax.set_title("voltage profile")
    ax.add_patch(plt.Circle((0, 0), radius=1.05, fill=False,
                            color='red', linewidth=0.5, linestyle='--'))
    ax.add_patch(plt.Circle((0, 0), radius=0.95, fill=False,
                            color='red', linewidth=0.5, linestyle='--'))
    ax.add_patch(plt.Circle((0, 0), radius=1.00, fill=False, color='green'))
    ax.plot(x[PQ.bus], y[PQ.bus], color='red', linestyle='none',
            marker='o', markersize=1.7, label='PQ bus')
    ax.plot(x[PV.bus], y[PV.bus], color='blue', linestyle='none',
            marker='o', markersize=3, label='PV bus')
    ax.plot(x[SW.bus], y[SW.bus], color='magenta', linestyle='none',
            marker='o', markersize=5, label='SW bus')
    if Bus.n < 100:
        ax.plot(x, y, color='black', linewidth=1.0, linestyle='-')
    # Remueve los ejes x e y
    ax.set_axis_off()
    # Remueve las líneas del marco de la figura
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    # Remueve el texto de los ejes
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    # ax.set_aspect('equal')
    # for i in range(len(x)-1):
    #         if i<=(Bus.n+1)/2:
    #                 angle=90-i/(Bus.n+1)*360
    #         else:
    #                 angle=-90-i/(Bus.n+1)*360
    #         ax.text(xTxT[i], yTxT[i], str(BusesNameExt[i]), rotation=0*theta[i]*180/np.pi)
    fig.set_facecolor('none')
    ax.legend()
    ############################################################
    return fig


def fcn_Plot_CAP(Bus, SW, PV):
    ############################################################
    Cap_Bus = np.concatenate((SW.con[:, 0], PV.con[:, 0]))
    if PV.n < 350:
        Cap_SN = np.concatenate((SW.con[:, 1], PV.con[:, 1]))/100
    else:
        Cap_SN = np.concatenate((SW.con[:, 1], PV.con[:, 11]))/100
    Cap_P = np.concatenate((Bus.ph[SW.bus], Bus.ph[PV.bus]))/Cap_SN
    Cap_Q = np.concatenate((Bus.qh[SW.bus], Bus.qh[PV.bus]))/Cap_SN
    Cap_S = np.sqrt(Cap_P**2+Cap_Q**2)
    idx_in = Cap_S < 1
    # ------------------------
    # fig, ax = plt.subplots(figsize=(10, 10), facecolor='none')
    fig, ax = plt.subplots()
    ax.set_title("capability curve of generators")
    ax.set_xlabel("Q [pu]")
    ax.set_ylabel("P [pu]")
    ax.add_patch(plt.Circle((0, 0), radius=1, fill=False, color='blue'))
    ax.scatter(Cap_Q[idx_in], Cap_P[idx_in], s=5 *
               Cap_SN[idx_in], facecolor='green')
    ax.scatter(Cap_Q[~idx_in], Cap_P[~idx_in],
               s=5*Cap_SN[~idx_in], facecolor='red')
    ax.scatter(Cap_Q[0], Cap_P[0], s=5*Cap_SN[0], facecolor='magenta')
    fig.set_facecolor('none')
    ax.grid(True)
    ax.set_axisbelow(True)
    # ax.axis([-1.1, 1.1, 0, 1.1])
    ax.set_xlim([min(min(Cap_Q)-0.1, -1.05), max(max(Cap_Q)+0.1, 1.05)])
    ax.set_ylim([min(min(Cap_P)-0.1, 0), max(max(Cap_P)+0.1, 1.05)])
    ax.set_aspect('equal')
     ############################################################
    return fig


def fcn_Plot_POW(Bus, SW, PV):
    ############################################################
    Cap_Bus = np.concatenate((SW.con[:, 0], PV.con[:, 0]))
    if PV.n < 350:
        Cap_SN = np.concatenate((SW.con[:, 1], PV.con[:, 1]))/100
    else:
        Cap_SN = np.concatenate((SW.con[:, 1], PV.con[:, 11]))/100
    Cap_P = np.concatenate((Bus.ph[SW.bus], Bus.ph[PV.bus]))/Cap_SN
    Cap_Q = np.concatenate((Bus.qh[SW.bus], Bus.qh[PV.bus]))/Cap_SN
    Cap_S = np.sqrt(Cap_P**2+Cap_Q**2)
    # ------------------------
    # fig, ax = plt.subplots(figsize=(10, 5), layout='constrained', facecolor='none')
    fig, ax = plt.subplots()
    ax.set_title("powers of generators")
    ax.set_xlabel("generators")
    ax.set_ylabel("power [pu]")
    ax.axhline(y=0, color='gray', linewidth=2, linestyle='-')
    ax.plot(np.arange(0, SW.n+PV.n), Cap_P, color='red', linewidth=1.0,
            linestyle='-', marker='o', markersize=2, label='P')
    ax.plot(np.arange(0, SW.n+PV.n), Cap_Q, color='blue', linewidth=1.0,
            linestyle='-', marker='o', markersize=2, label='Q')
    ax.plot(np.arange(0, SW.n+PV.n), Cap_S, color='black', linewidth=1.0,
            linestyle='-', marker='o', markersize=2, label='S')
    fig.set_facecolor('none')
    ax.legend()
    ax.grid(True)
    ax.set_axisbelow(True)
    ax.set_xlim([0, SW.n+PV.n-1])
    if Bus.n < 100:
        # plt.xticks(range(len(x)), range(1, len(x)+1))
        plt.xticks(np.arange(0, SW.n+PV.n), Cap_Bus.astype(int), rotation=90)
     ############################################################
    return fig


# --------------------------------------------------------------------
# plt.suptitle("voltage profile")
# plt.title("voltage profile")
# plt.xlabel("buses")
# plt.ylabel("voltage [pu]")
# plt.legend(xxxxxx,loc='upper left')
# plt.xticks(Buses,BusesName)
# plt.savefig('C:/Users/Usuario/Desktop/Test.png')
# plt.axis([1, Bus.n, 0.9, 1.1])
# plt.plot(Buses, Bus.vh, color='black', linewidth=3.0)
# plt.show()

# plt.clf()
# plt.cla()

# graph = pd.DataFrame(vect_data,vect_iter)
# graph.plot(kind='line')
# --------------------------------------------------------------------
