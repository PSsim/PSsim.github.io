import numpy as np
import plotly.graph_objects as go
import plotly.express as px


def fcn_Plot_VPi(Bus, SW, PV, PQ):
    ############################################################
    Buses = np.arange(1, Bus.n+1)
    # ------------------------
    # Create traces
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=Buses, y=1.05*np.ones(Bus.n), mode='lines', name='+5%',line=dict(color='red', width=0.5,dash='dash')))  # 'dash', 'dot', and 'dashdot'
    fig.add_trace(go.Scatter(x=Buses, y=0.95*np.ones(Bus.n), mode='lines', name='-5%',line=dict(color='red', width=0.5,dash='dash')))
    fig.add_trace(go.Scatter(x=Buses, y=Bus.vh, mode='lines', name='profile',line=dict(color='black', width=1)))
    fig.add_trace(go.Scatter(x=Buses[PQ.bus], y=Bus.vh[PQ.bus],mode='markers', name='PQ bus',marker_size=3,line=dict(color='red')))
    fig.add_trace(go.Scatter(x=Buses[PV.bus], y=Bus.vh[PV.bus],mode='markers', name='PV bus',marker_size=6,line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=Buses[SW.bus], y=Bus.vh[SW.bus],mode='markers', name='SW bus',marker_size=9,line=dict(color='magenta')))
    # Edit the layout
    fig.update_layout(title='voltage profile',xaxis_title='buses',yaxis_title='voltage [pu]')
    fig.update_layout(
        xaxis=dict(
            # showline=True,
            showgrid=False,
            # showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            # zeroline=False,
            ticks='outside',
            # tickfont=dict(family='Arial',size=12, color='rgb(82, 82, 82)',),
        ),
        yaxis=dict(
            showgrid=False,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            # zeroline=False,
            # showline=False,
            # showticklabels=False,
        ),
    #     autosize=False,margin=dict(autoexpand=False,l=100,r=20,t=110,),
    #     showlegend=True,
    #     plot_bgcolor='magenta'
    )
    fig.update_xaxes(range=list([1,Bus.n]))
    fig.update_yaxes(range=list([0.95*min(Bus.vh),1.05*max(Bus.vh)]))
    ############################################################
    return fig


def fcn_Plot_VPC_ly(Bus, SW, PV, PQ):
    ############################################################
    radius = np.concatenate([Bus.vh, [Bus.vh[0]]])
    theta = np.linspace(5*np.pi/2, np.pi/2, Bus.n+1)
    x = radius*np.cos(theta)
    y = radius*np.sin(theta)
    # ------------------------
    rad095 = 0.95
    rad105 = 1.05
    rad100 = 1.00
    # ------------------------
    # Create traces
    fig = go.Figure()
    fig.add_shape(type='circle',x0=-rad095, y0=-rad095, x1=rad095, y1=rad095, name='+5%',line=dict(color='red', width=0.5,dash='dash'))  # 'dash', 'dot', and 'dashdot'
    fig.add_shape(type='circle',x0=-rad105, y0=-rad105, x1=rad105, y1=rad105, name='-5%',line=dict(color='red', width=0.5,dash='dash'))
    fig.add_shape(type='circle',x0=-rad100, y0=-rad100, x1=rad100, y1=rad100, name='base',line=dict(color='green', width=1))
    fig.add_trace(go.Scatter(x=x[PQ.bus], y=y[PQ.bus],mode='markers', name='PQ bus',marker_size=3,line=dict(color='red'), hoverinfo='skip'))
    fig.add_trace(go.Scatter(x=x[PV.bus], y=y[PV.bus],mode='markers', name='PV bus',marker_size=6,line=dict(color='blue'), hoverinfo='skip'))
    fig.add_trace(go.Scatter(x=x[SW.bus], y=y[SW.bus],mode='markers', name='SW bus',marker_size=9,line=dict(color='magenta'), hoverinfo='skip'))
    if Bus.n < 100:
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='voltage',
                            line=dict(color='white', width=1),customdata=radius,
                            hovertemplate='voltage: %{customdata:.3f}'))
    # ------------------------
    # Edit the layout
    fig.update_layout(title='voltage profile',showlegend=True)
    # fig.update_layout(width=800, height=800)
    # Remover ejes x e y
    fig.update_xaxes(showticklabels=False)
    fig.update_xaxes(zeroline=False)
    fig.update_yaxes(showticklabels=False)
    fig.update_yaxes(zeroline=False)
    # Remover líneas del marco de la figura
    fig.update_xaxes(showline=False)
    fig.update_yaxes(showline=False)
    # Remover grilla
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    # Colores de fondo
    fig.update_layout(plot_bgcolor='black',paper_bgcolor='rgba(0,0,0,0)')
    # Aspect Ratio
    fig.update_yaxes(scaleanchor="x",scaleratio=1)
    ############################################################
    return fig


def fcn_Plot_PX(Bus):
    ############################################################
    Buses = np.arange(1, Bus.n+1)
    # fig = px.scatter(x=Buses, y=Bus.vh, color=Bus.vh, hover_name=BusesName, color_continuous_scale='bluered_r')   # , size=Bus.vh
    fig = px.line(x=Buses, y=Bus.vh, title='voltage profile',markers=True)   # , color=Bus.vh
    # fig = px.bar(x=Buses, y=Bus.vh, color=Bus.vh,
    #              color_continuous_scale='bluered_r')   # 'ice' 'bluered' 'bluered_r'
    fig.show()
    ############################################################
    return fig