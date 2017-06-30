import plotly
import plotly.plotly as py
from plotly.graph_objs import *
import pandas as pd
from plotly.graph_objs import Scatter, Layout

plotly.offline.init_notebook_mode(connected=True)

mapbox_access_token = 

data = Data([
    Scattermapbox(
        lat=['41.38635837'],
        lon=['2.15977143'],
        mode='markers',
        marker=Marker(
            size=14
        ),
        text=['biercab-barcelona'],
    )
])

layout = Layout(
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=41,
            lon=2
        ),
        pitch=0,
        zoom=5
    ),
)

fig = dict(data=data, layout=layout)
plotly.offline.iplot(fig, filename='Barcelona Mapbox')
