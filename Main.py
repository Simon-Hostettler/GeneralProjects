from plotly.offline import plot
from plotly.graph_objs import *

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

graph = graph_objs.Histogram2dContour(name = "Mouse movement Heatmap",
                               x = x,
                               y = y,
                               contours = dict(showlines = False),
                               xbins = dict(start = 0,
                                            size = 50,
                                            end = 1920),
                               ybins = dict(start=0,
                                            size = 50,
                                            end=1080),
                               colorscale = [[0, 'rgb(0,0,255)'], [0.5, 'rgb(255,255,0)'], [1, 'rgb(255,0,0)']],
                               showscale = True)

trace = [graph]
fig = graph_objs.Figure(data = trace)
plot(fig, show_link=False)
