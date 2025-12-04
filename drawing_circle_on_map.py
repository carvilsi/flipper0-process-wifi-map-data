import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from math import radians, cos, sin, asin, sqrt, pi

def generate_circle_points(lat, lon, radius, name):
    # parameters
    N = 360 # number of discrete sample points to be generated along the circle
    
    # generate points
    circle_lats, circle_lons = [], []
    circle_names = []
    for k in range(N):
        # compute
        angle = pi*2*k/N
        dx = radius*cos(angle)
        dy = radius*sin(angle)
        circle_lats.append(lat + (180/pi)*(dy/6378137))
        circle_lons.append(lon + (180/pi)*(dx/6378137)/cos(lat*pi/180))
        circle_names.append(name)
    circle_lats.append(circle_lats[0])
    circle_lons.append(circle_lons[0])
    return (circle_lats, circle_lons, circle_names)

def draw_circle(circle_lats, circle_lons, circle_names, fig):
    fig.add_trace(go.Scattermap(
        lat=circle_lats,
        lon=circle_lons,
        text=circle_names,
        mode='lines',
        marker=go.scattermap.Marker(
            size=1,
            color="BlueViolet",
        ),
    ))

df = pd.read_csv("geo_data.csv")

fig = px.scatter_map(
        df,
        lon="longitude",
        lat="latitude",
        hover_name="ap_hash", 
        hover_data=["ap_hash", "time"],
        zoom=16,
        width=800,
        height=800,
        )


for i in range(0,len(df)):
    (circle_lats, circle_lons, circle_names) = generate_circle_points(df.latitude[i], df.longitude[i], 5, df.ap_hash[i])
    draw_circle(circle_lats, circle_lons, circle_names, fig)

fig.update_layout(
        map_style="carto-darkmatter-nolabels",
        )

fig.show()
