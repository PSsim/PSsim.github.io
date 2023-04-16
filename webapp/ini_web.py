from kernel.appRead import fcn_Read
from kernel.appSim import fcn_Sim
from kernel.appPlotPF_bokeh import fcn_Plot_VP_bokeh, fcn_Plot_VPC_bokeh, fcn_Plot_CAP_bokeh
from kernel.appPlotPF_NX import fcn_Plot_NX
# from kernel.appPlotPF_matplotlib import fcn_Plot_VP, fcn_Plot_VPC, fcn_Plot_CAP, fcn_Plot_POW
# import numpy as np
# import js


# BOKEH
import json
import pyodide

from js import Bokeh, JSON  # , console

from bokeh.embed import json_item
from bokeh.resources import CDN


def Load_and_PFsolver(Element, FileName):
    ############################################################
    LNdata, SHdata, SWdata, PVdata, PQdata = fcn_Read(FileName)
    # ------------------------
    Element('dataLN-txt').element.value = LNdata[0]
    Element('dataSH-txt').element.value = SHdata[0]
    Element('dataSW-txt').element.value = SWdata[0]
    Element('dataPV-txt').element.value = PVdata[0]
    Element('dataPQ-txt').element.value = PQdata[0]
    # ------------------------
    global Dims
    Dims = [LNdata[1], SHdata[1], SWdata[1], PVdata[1], PQdata[1]]
    # ------------------------
    fcn_PFsolver(Element)
    ############################################################


def fcn_PFsolver(Element):
    ############################################################
    dataLN_str = Element('dataLN-txt').element.value
    dataSH_str = Element('dataSH-txt').element.value
    dataSW_str = Element('dataSW-txt').element.value
    dataPV_str = Element('dataPV-txt').element.value
    dataPQ_str = Element('dataPQ-txt').element.value
    # # ------------------------
    FLAG, Mx, Bus, SW, PV, PQ, Line = fcn_Sim(
        dataLN_str, dataSH_str, dataSW_str, dataPV_str, dataPQ_str, Dims)
    # ------------------------
    # MyinputValor = float(Myinput.value)
    # ------------------------
    # Element('MiResultadoDIV').write(PF_table)
    Element('HOLA').write(FLAG)
    # ------------------------

    # ------------------------
    #  Matplotlib Plots
    # aux1 = fcn_Plot_VP(Bus, SW, PV, PQ)
    # aux2 = fcn_Plot_VPC(Bus, SW, PV, PQ)
    # aux3 = fcn_Plot_CAP(Bus, SW, PV)
    # aux4 = fcn_Plot_POW(Bus, SW, PV)
    # display(aux1, target='myplot5')
    # display(aux2, target='Plot_VPC')
    # display(aux3, target='Plot_CAP')
    # display(aux4, target='myplot6')
    # ------------------------

    Plot_VP_bokeh = fcn_Plot_VP_bokeh(Bus, SW, PV, PQ)
    Plot_VPC_bokeh = fcn_Plot_VPC_bokeh(Bus, SW, PV, PQ)
    Plot_CAP_bokeh = fcn_Plot_CAP_bokeh(Bus, SW, PV, PQ)
    Plot_NX = fcn_Plot_NX(Line)

    Bokeh.embed.embed_item(JSON.parse(
        json.dumps(json_item(Plot_VP_bokeh, "myplot1"))))
    Bokeh.embed.embed_item(JSON.parse(
        json.dumps(json_item(Plot_VPC_bokeh, "myplot2"))))
    Bokeh.embed.embed_item(JSON.parse(
        json.dumps(json_item(Plot_CAP_bokeh, "myplot3"))))
    Bokeh.embed.embed_item(JSON.parse(
        json.dumps(json_item(Plot_NX, "myplot4"))))
    ############################################################
