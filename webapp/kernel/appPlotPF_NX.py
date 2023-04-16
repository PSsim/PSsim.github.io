import networkx as nx
from bokeh.plotting import from_networkx
from bokeh.models.tools import HoverTool, Range1d
from bokeh.models import Plot, MultiLine, Circle
from bokeh.models.graphs import NodesAndLinkedEdges


def fcn_Plot_NX(Line):
    ############################################################
    edge_list = list(zip(Line.fr+1, Line.to+1, Line.con[:, 8]))
    # Graph, DiGraph, MultiGraph, MultiDiGraph
    G = nx.MultiGraph()
    G.add_edges_from(edge_list)

    p = Plot()
    p.x_range = Range1d(-1.05, 1.05)
    p.y_range = Range1d(-1.05, 1.05)
    # spring_layout, circular_layout, shell_layout, spectral_layout, planar_layout
    g = from_networkx(G, nx.circular_layout, scale=1, center=(0, 0))
    p.renderers.append(g)

    g.node_renderer.glyph = Circle(size=10, fill_color='blue')
    g.edge_renderer.glyph = MultiLine(
        line_color='blue', line_alpha=0.5, line_width=3)

    g.node_renderer.hover_glyph = Circle(size=10, fill_color='red')
    g.edge_renderer.hover_glyph = MultiLine(line_color='red', line_width=10)

    g.inspection_policy = NodesAndLinkedEdges()

    p.add_tools(HoverTool(tooltips=None))
    # ------------------------

    # ------------------------
    color_oscuro = '#1a1a1a'
    color_claro = 'rgb(230, 230, 230)'
    # ------------------------
    p.toolbar.autohide = True
    # 'stretch_both', 'stretch_width', 'stretch_height'
    p.sizing_mode = 'stretch_width'
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
    p.title.text_color = color_claro
    p.grid.grid_line_alpha = 0.2
    ############################################################
    return p
