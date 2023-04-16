import numpy as np
import pandas as pd
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models.tools import HoverTool, Range1d, BoxAnnotation


# 220  53  69  #dc3545 (RED)
#  13 110 253  #0d6efd (BLUE)
#  40 167  69  #28a745 (GREEN)
# 255 193   7  #ffc107 (YELLOW)
#  23 162 184  #17a2b8 (CYAN)
# 102  16 242  #6610f2 (INDIGO)
# 253 126  20  #fd7e14 (ORANGE)
# 111  66 193  #6f42c1 (PURPLE)
# 214  51 132  #d63384 (PINK)
#  32 201 151  #20c997 (TEAL)
color_oscuro = '#1a1a1a'
color_claro = 'rgb(230, 230, 230)'
color_SW = '#0d6efd'
color_PV = '#28a745'
color_PQ = '#dc3545'


def My_Bokeh_Style(p):
    ############################################################
    p.toolbar.autohide = True
    p.sizing_mode='stretch_width'   # 'stretch_both', 'stretch_width', 'stretch_height'
    # p.width = 1000
    # p.height = 500
    # ------------------------
    p.background_fill_color = color_oscuro
    p.border_fill_color = None    # None
    p.outline_line_color = color_claro
    p.axis.major_label_text_color = color_claro
    p.axis.axis_label_text_color = color_claro
    p.axis.major_tick_line_color = color_claro
    p.axis.minor_tick_line_color = color_claro
    p.axis.axis_line_color = color_claro
    p.legend.label_text_color = color_claro
    p.legend.background_fill_color = 'rgba(55, 55, 55, 0.5)'
    p.legend.border_line_color = color_claro
    p.title.text_color = color_claro
    p.grid.grid_line_alpha = 0.2
    ############################################################
    return p


def fcn_Plot_VP_bokeh(Bus, SW, PV, PQ):
    ############################################################
    aux = np.arange(Bus.n)
    PF_table = np.concatenate((np.arange(1, Bus.n+1).reshape(-1, 1),
                               Bus.con[aux, 0].reshape(-1, 1),
                               Bus.ph[aux].reshape(-1, 1),
                               Bus.qh[aux].reshape(-1, 1),
                               Bus.vh[aux].reshape(-1, 1),
                               Bus.ah[aux].reshape(-1, 1)*180/np.pi), axis=1)
    # ------------------------
    df = pd.DataFrame(PF_table, columns=["num", "bus", "ph", "qh", "vh", "ah"])
    source = ColumnDataSource(data=df)
    # ------------------------
    p = figure(tools='box_zoom, xwheel_zoom, save, reset')     # pan, zoom_in, zoom_out, xzoom_out, xzoom_in, box_select,  tools=''
    p.title = 'voltage profile'
    p.xaxis.axis_label = 'buses'
    p.yaxis.axis_label = 'voltage [pu]'
    p.x_range = Range1d(1, Bus.n)
    p.y_range = Range1d(0.95*min(Bus.vh), 1.05*max(Bus.vh))
    # ------------------------
    Buses = np.arange(1, Bus.n+1)
    # p.line(Buses, 1.05*np.ones(Bus.n), line_width=0.5, color='red', line_dash='dashed')   # dashed, dotted, dotdash, dashdot
    # p.line(Buses, 0.95*np.ones(Bus.n), line_width=0.5, color='red', line_dash='dashed')
    p.add_layout(BoxAnnotation(bottom=0.95, top=1.05, fill_alpha=0.1, fill_color='#28a745'))
    p.line(x="num", y="vh", source=source, line_width=1, color=color_claro,legend_label='profile',name='LineTips')
    p.circle(Buses[PQ.bus], Bus.vh[PQ.bus],color=color_PQ,legend_label='PQ bus',size=2)
    p.circle(Buses[PV.bus], Bus.vh[PV.bus],color=color_PV,legend_label='PV bus',size=4)
    p.circle(Buses[SW.bus], Bus.vh[SW.bus],color=color_SW,legend_label='SW bus',size=6)
    # ------------------------
    p.legend.orientation = 'horizontal'   # vertical, horizontal
    p.legend.location = 'top_right'
    p.legend.click_policy = 'hide'
    p.legend.inactive_fill_color = 'rgb(60, 60, 60)'
    # p.legend.label_text_font_size = '20px'
    # ------------------------
    # p.grid.grid_line_dash = [6, 4]
    p.grid.visible = False  # p.grid.visible  p.xgrid.visible   p.ygrid.visible
        # ------------------------
    hover = HoverTool(renderers=[p.select(name='LineTips')[0]])   # HoverTool()
    # hover.tooltips = """
    #     <h4>bus: @bus</h4>
    #     <h4>v: @vh</h4>
    #     <h4>p: @ph, q: @qh</h4>
    #     """
    TOOLTIPS = [
    ("bus", "@bus"),
    ('voltage', '@vh'),
    ('p, q', '@ph{0.000}, @qh{0.000}')
    ]
    hover.tooltips = TOOLTIPS
    p.add_tools(hover)
    p = My_Bokeh_Style(p)
    ############################################################
    return p


def fcn_Plot_VPC_bokeh(Bus, SW, PV, PQ):
    ############################################################
    busname = np.concatenate([Bus.con[:, 0], [Bus.con[0, 0]]])
    radius = np.concatenate([Bus.vh, [Bus.vh[0]]])
    theta = np.linspace(5*np.pi/2, np.pi/2, Bus.n+1)
    x = radius*np.cos(theta)
    y = radius*np.sin(theta)
    thetaAux = np.linspace(5*np.pi/2, np.pi/2, 200)
    # ------------------------
    aux = np.concatenate((x.reshape(-1, 1),y.reshape(-1, 1),radius.reshape(-1, 1),busname.reshape(-1, 1)), axis=1)
    df = pd.DataFrame(aux, columns=["x", "y", "radius", "busname"])
    source = ColumnDataSource(data=df)
    # ------------------------
    p = figure(tools='box_zoom, xwheel_zoom, save, reset')     # pan, zoom_in, zoom_out, xzoom_out, xzoom_in, box_select,  tools=''
    p.title = 'voltage profile'
    p.axis.visible = False
    p.grid.visible = False
    # ------------------------
    p.line(1.05*np.cos(thetaAux), 1.05*np.sin(thetaAux), line_width=0.5, color='#dc3545', line_dash='dashed') # dashed, dotted, dotdash, dashdot
    p.line(0.95*np.cos(thetaAux), 0.95*np.sin(thetaAux), line_width=0.5, color='#dc3545', line_dash='dashed')
    p.line(1.00*np.cos(thetaAux), 1.00*np.sin(thetaAux), line_width=1.0, color='#28a745')
    p.line(x="x", y="y", source=source, line_width=1, color=color_claro,legend_label='profile',name='LineTips')
    p.circle(x[PQ.bus], y[PQ.bus], color=color_PQ,legend_label='PQ bus',size=2)
    p.circle(x[PV.bus], y[PV.bus], color=color_PV,legend_label='PV bus',size=4)
    p.circle(x[SW.bus], y[SW.bus], color=color_SW,legend_label='SW bus',size=6)
        # ------------------------
    # p.legend.orientation = 'vertical'   # vertical, horizontal
    p.legend.location = 'top_right'
    p.legend.click_policy = 'hide'
    p.legend.inactive_fill_color = 'rgb(60, 60, 60)'
    # ------------------------
    hover = HoverTool(renderers=[p.select(name='LineTips')[0]])
    TOOLTIPS = [
    ("bus", "@busname"),
    ('voltage', '@radius')
    ]
    hover.tooltips = TOOLTIPS
    p.add_tools(hover)
    p = My_Bokeh_Style(p)
    ############################################################
    return p


def fcn_Plot_CAP_bokeh(Bus, SW, PV, PQ):
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
    SizeAux = 30*Cap_SN/max(Cap_SN)
    SizeAux[SizeAux<3] = 3
    # ------------------------
    aux = np.concatenate((Cap_Bus.reshape(-1, 1),Cap_P.reshape(-1, 1),Cap_Q.reshape(-1, 1),SizeAux.reshape(-1, 1)), axis=1)
    df = pd.DataFrame(aux, columns=["busname", "p", "q", "SizeSN"])
    # dfin = df.loc[idx_in, ["busname", "p", "q"]]
    dfin = df.loc[idx_in, :]
    dfou = df.loc[~idx_in, :]
    source_in = ColumnDataSource(dfin)
    source_ou = ColumnDataSource(dfou)
    # ------------------------
    p = figure(tools='box_zoom, xwheel_zoom, save, reset')     # pan, zoom_in, zoom_out, xzoom_out, xzoom_in, box_select,  tools=''
    p.title = 'capability curve of generators'
    p.xaxis.axis_label = 'Q [pu]'
    p.yaxis.axis_label = 'P [pu]'
    p.x_range = Range1d(min(min(Cap_Q)-0.1, -1.05), max(max(Cap_Q)+0.1, 1.05))
    p.y_range = Range1d(min(min(Cap_P)-0.1, 0), max(max(Cap_P)+0.1, 1.05))
    # ------------------------
    # p.circle(df['q'][idx_in], df['p'][idx_in],legend_label='normal', color='#28a745',size=3)
    thetaAux = np.linspace(5*np.pi/2, np.pi/2, 200)
    p.line(1.00*np.cos(thetaAux), 1.00*np.sin(thetaAux), line_width=2.0, color='#17a2b8')
    # p.circle(Cap_Q[idx_in], Cap_P[idx_in],legend_label='normal', color='#28a745',size=1*Cap_SN[idx_in])
    # p.circle(Cap_Q[~idx_in], Cap_P[~idx_in],legend_label='overload', color='#dc3545',size=1*Cap_SN[~idx_in])
    p.circle(x="q", y="p",source=source_in,legend_label='normal'  , color='#28a745',size="SizeSN",name='LineTips',muted_alpha=0.2)
    p.circle(Cap_Q[0], Cap_P[0],legend_label='SW bus', color=color_SW,size=SizeAux[0],muted_alpha=0.2)
    p.circle(x="q", y="p",source=source_ou,legend_label='overload', color='#dc3545',size="SizeSN",name='LineTips',muted_alpha=0.2)
    # ------------------------
    # p.legend.location = 'top_right'
    p.legend.click_policy = 'mute'
    p.legend.inactive_fill_color = 'rgb(60, 60, 60)'
    # ------------------------
    hover = HoverTool(renderers=[r for r in p.renderers if r.name == 'LineTips'])
    TOOLTIPS = [
    ("bus", "@busname"),
    ('p, q', '@p{0.000}, @q{0.000}')
    ]
    hover.tooltips = TOOLTIPS
    p.add_tools(hover)
    p = My_Bokeh_Style(p)
    ############################################################
    return p