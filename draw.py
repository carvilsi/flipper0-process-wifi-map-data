import plotly.express as px
import pandas as pd

df = pd.read_csv("data.csv")

df.dropna(
    axis=0,
    how='any',
    # thresh=None,
    subset=None,
    inplace=True
)

color_scale = [(0, 'orange'), (1,'red')]

# fig = px.scatter_mapbox(df, 
fig = px.scatter_map(df, 
                        lat="Lat", 
                        lon="Long", 
                        hover_name="Address", 
                        hover_data=["Address", "Listed"],
                        # color="Listed",
                        # color_continuous_scale=color_scale,
                        # size="Listed",
                        opacity=1,
                        zoom=16, 
                        height=800,
                        width=800,
                        map_style="carto-darkmatter-nolabels")
                        # map_style="carto-voyager-nolabels")
                        # map_style="carto-darkmatter")
                        # map_style="dark")
                        # map_style="open-street-map")

# fig.update_layout(mapbox_style="open-street-map")
# fig.update_layout(mapbox_style="satellite")
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
# fig.show(renderer="png")
