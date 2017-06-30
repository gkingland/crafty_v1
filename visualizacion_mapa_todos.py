#Shows a map with all the craft beer pubs in Barcelona
import plotly
import plotly.plotly as py
from plotly.graph_objs import *
from pymongo import Connection
from pymongo import MongoClient
from bson.json_util import dumps

plotly.offline.init_notebook_mode(connected=True)

#conection to DB with yelp information about pubs

connection = Connection ('localhost', 27017)
db = connection.CByelp2
collection = db.cbs

longitud = []
latitud = []
datos = []
name = []

#Formateado los datos a la estructura adecuada
cursor = collection.find()
for b in cursor:
    datos = b["loc"]
    nombre = b["name"]
    longitud.append(datos[0])
    latitud.append(datos [1])
    name.append(dumps(nombre))
    
#Utilizando Plotly
mapbox_access_token = 

#colocar todas las latitudes y todas las longitudes en uno solo
data = Data([
    Scattermapbox(
        lat=latitud,
        lon=longitud,
        mode='markers',
        marker=Marker(
            size=9
        ),
        text=name
    )
])
layout = Layout(
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=41.38,
            lon=2.15
        ),
        pitch=0,
        zoom=10
    ),
)

fig = dict(data=data, layout=layout)
plotly.offline.iplot(fig, filename='Multiple Mapbox')