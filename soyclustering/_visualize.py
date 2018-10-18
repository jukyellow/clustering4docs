from bokeh.models import HoverTool
from bokeh.models import ColumnDataSource
from bokeh.palettes import Greys256
from sklearn.metrics import pairwise_distances


def center_to_bokeh_heatmap(centers, cluster_idx, palettes=None):

    def get_color(dist, palettes, max_=1):
        idx = int( (len(palettes)-1) * dist / max_ )
        idx = min(idx, len(palettes)-1)
        return palettes[idx]

    if palettes is None:
        palettes = Greys256

    n_clusters = centers.shape[0]
    pdist = pairwise_distances(centers, metric='cosine')

    xname = []
    yname = []
    color = []
    names = ['cluster {}'.format(cluster_idx[i]) for i in range(n_clusters)]

    for i in range(n_clusters):
        for j in range(n_clusters):
            xname.append('cluster {}'.format(cluster_idx[i]))
            yname.append('cluster {}'.format(cluster_idx[j]))
            color.append(get_color(pdist[i,j], palettes))

    source = ColumnDataSource(data=dict(
        xname=xname,
        yname=yname,
        colors=color,
        cos=pdist.flatten()
    ))

    p = figure(title="Cluster center pairwise distance",
           x_axis_location="above", x_range=names, y_range=names,
           tools="hover,save,wheel_zoom,box_zoom,reset")

    p.plot_width = 800
    p.plot_height = 800
    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_text_font_size = "5pt"
    p.axis.major_label_standoff = 0
    p.xaxis.major_label_orientation = np.pi/3

    p.rect('xname', 'yname', 0.9, 0.9, source=source,
           color='colors', line_color=None,
           hover_line_color='black', hover_color='colors')

    p.select_one(HoverTool).tooltips = [
        ('names', '@yname, @xname'),
        ('cos', '@cos'),
    ]

    return p