import matplotlib.pyplot as plt
import numpy as np
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.graph_objs import Scatter, Figure, Layout
from plotly.graph_objs import *

#here's our data to plot, all normal Python lists

with open("Mouseevents.txt", "r") as f:
    x = []
    y = []
    content = f.read()
    fullarray = content.split(",")
    counter = 0
    for coordinates in fullarray:
        if counter % 2 == 0:
            x.append(coordinates)
        else:
            y.append(coordinates)
        counter += 1

print(len(x))
print(len(y))

layout = graph_objs.Layout(
    xaxis=dict(
        range=[0, 1920]
    ),
    yaxis=dict(
        range=[0, 1080]
    )
)
fig = graph_objs.Figure(data = [Histogram2dContour(x=x, y=y, contours=Contours(coloring='heatmap'))], layout = layout)
plot(fig, show_link=False)
