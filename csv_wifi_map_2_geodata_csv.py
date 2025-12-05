#!/usr/bin/env python

# This script generates a geospatial CSV data
# and draws a map (openstreetmap)
# Example of command:
# python csv_wifi_map_2_geodata_csv.py local-data/wifi_map_6-10-2025_19_19_26_home_consum.csv '39.661423,-0.226952' '39.663005,-0.225719'

import csv
import sys
import math
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from math import radians, cos, sin, asin, sqrt, pi

RADIUS_EARTH = 6378.137 * 1000


def calculate_angle(coord):
    m = (coord[1]["y"] - coord[0]["y"]) / (coord[1]["x"] - coord[0]["x"])
    alpha = math.atan(m)
    return alpha


def get_coordinates():
    origin_coords = sys.argv[2].split(",")
    origin_coord = {"x": float(origin_coords[0]), "y": float(origin_coords[1])}
    end_coords = sys.argv[3].split(",")
    end_coord = {"x": float(end_coords[0]), "y": float(end_coords[1])}
    return (origin_coord, end_coord)


def calculate_new_coordinates(coord, dist, alpha):
    dx = float(dist) * math.sin(alpha)
    dy = float(dist) * math.cos(alpha)
    # coord[0] is the latitude and longitude for starting point
    new_lat = float(coord[0]["x"]) + (dy / RADIUS_EARTH) * (180 / math.pi)
    new_lon = float(coord[0]["y"]) + (
        (dx / RADIUS_EARTH) * (180 / math.pi) / math.cos(coord[0]["x"] * math.pi / 180)
    )
    return (new_lat, new_lon)

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

def main():
    if len(sys.argv) != 4:
        raise Exception("""
        You must provide a FlipperZero WiFi Map csv file and
        start and end maps coordinates""")

    # get coordinates from command line argument
    coordinates = get_coordinates()
    # calculate the angle for direction
    angle = calculate_angle(coordinates)

    # where to store the processed geo data
    geo_data = []

    # Process the data from WiFi Map CSV file from FlipperZero
    df = pd.read_csv(sys.argv[1], sep=";")

    times = df["Time from start (seconds)"].unique()

    # splitting the data base on same moment adquisition
    subsets = []
    for tm in times:
        sub = df.loc[df["Time from start (seconds)"] == tm]
        subsets.append(sub)


    # get an array holding all the nearest APs
    nearests_uniq = []
    for sub in subsets:
        ap_hash = sub.iloc[0, 0]
        if len(nearests_uniq) == 0:
            nearests_uniq.append(ap_hash)
        else:
            if ap_hash not in nearests_uniq:
                nearests_uniq.append(ap_hash)

    # get all data related with the nearest APs
    interest_aps = []
    for closer in nearests_uniq:
        interest_aps.append(df.loc[df["AP hash"] == closer])

    # Calculating the coordenates
    # total distance walked
    walked_distance = 0
    time = 0
    delta_dst = 0
    ap_hash = ""
    for i, aps in enumerate(interest_aps):
        if i == 0:
            walked_distance += interest_aps[i].tail(1).iloc[0, 1]
            time = interest_aps[i].tail(1).iloc[0, 3]
            ap_hash = interest_aps[i].tail(1).iloc[0, 0]
            dict_geo_data = {
                "ap_hash": ap_hash,
                "latitude": float(coordinates[0]["x"]),
                "longitude": float(coordinates[0]["y"]),
                "time": int(time),
                "val": 100,
            }
            geo_data.append(dict_geo_data)
        else:
            row = interest_aps[i].loc[df["Time from start (seconds)"] == time]
            if not row.empty:
                latest_row = interest_aps[i].tail(1)
                time = latest_row.iloc[0, 3]
                ap_hash = latest_row.iloc[0, 0]
                start_dst = row.iloc[0, 1]
                end_dst = latest_row.iloc[0, 1]
                delta_dst = abs(start_dst - end_dst)
                walked_distance += delta_dst
                if len(interest_aps) - 1 == i:
                    walked_distance += end_dst
                    delta_dst = end_dst

                (new_lat, new_lon) = calculate_new_coordinates(
                    coordinates, walked_distance, angle
                )
                dict_geo_data = {
                    "ap_hash": ap_hash,
                    "latitude": round(new_lat, 10),
                    "longitude": round(new_lon, 10),
                    "time": int(time),
                    "val": 100,
                }
                geo_data.append(dict_geo_data)

    # lets save the data on a csv for later drawing
    with open("geo_data.csv", "w", newline="") as csv_geo_data:
        headers = ["ap_hash", "latitude", "longitude", "time", "val"]
        writer = csv.DictWriter(csv_geo_data, fieldnames=headers)
        writer.writeheader()
        writer.writerows(geo_data)

    gdf = pd.read_csv("geo_data.csv")

    gdf.dropna(axis=0, how="any", subset=None, inplace=True)

    fig = px.scatter_map(
        gdf,
        lat="latitude",
        lon="longitude",
        hover_name="ap_hash",
        hover_data=["ap_hash", "time"],
        zoom=17,
        height=850,
        width=850,
    )

    # Drawing sorrunding APs
    for i, ap_draw in gdf.iterrows():
        # if i > 0:
        for j, sub in enumerate(subsets):
            row = sub.loc[(sub["AP hash"] == ap_draw["ap_hash"]) & (sub["Time from start (seconds)"] == ap_draw["time"])]
            
            if not row.empty:
                print("--- ROW ---")
                print(row[["AP hash", "Time from start (seconds)"]])
                print("-----------")
                print(sub)
                print("|=0=|")
                for s, aps in sub.iterrows():
                # APs that were on same time

                    (circle_lats, circle_lons, circle_names) = generate_circle_points(ap_draw.latitude, ap_draw.longitude, aps["Distance (meters)"], aps["AP hash"])
                    draw_circle(circle_lats, circle_lons, circle_names, fig)
    
    fig.update_layout(map_style="carto-darkmatter-nolabels")


    fig.show()
    print("Process and drawing done, visit your default browser")


if __name__ == "__main__":
    main()
