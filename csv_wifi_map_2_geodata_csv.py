#!/usr/bin/env python

# This script generates a geospatial CSV data
# and draws a map (openstreetmap)

import csv
import sys
import math
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from math import cos, sin, pi
import argparse

parser = argparse.ArgumentParser(description="Process the colected APs data on FlipperZero and draws the the points on OpenStreetMap map\n\te.g. ./cliprog.py path/to/csv '39.635191,-0.239454' '39.635192,-0.239455'")

parser.add_argument("csv_wifi_map", help="path to the csv WiFi-Map file from FlipperZero")
parser.add_argument("start_coordinates", help="The start cordinates point, 'latitude,longitde' you can get this on https://www.openstreetmap.org using 'Center Map here' and getting it from url; e.g. '39.635191,-0.239454'")
parser.add_argument("end_coordinates", help="The end cordinates point, 'latitude,longitde' you can get this on https://www.openstreetmap.org using 'Center Map here' and getting it from url; e.g. '39.635192,-0.239455'")
parser.add_argument("-dc", "--draw_circles", help="If set will draw circles with estimated distance to the AP", action="store_true")
parser.add_argument("-o", "--output_geo_csv_file", help="Saves the processed data on CSV file")

args = parser.parse_args()

# VIC (Very Important Constants)
RADIUS_EARTH = 6378.137 * 1000
N = 360 # number of discrete sample points to be generated along the circle
SEMI_C = 180


def calculate_angle(coord):
    m = (coord[1]["y"] - coord[0]["y"]) / (coord[1]["x"] - coord[0]["x"])
    alpha = math.atan(m)
    return alpha


def get_coordinates():
    origin_coords = args.start_coordinates.split(",")
    origin_coord = {"x": float(origin_coords[0]), "y": float(origin_coords[1])}
    end_coords = args.end_coordinates.split(",")
    end_coord = {"x": float(end_coords[0]), "y": float(end_coords[1])}
    return (origin_coord, end_coord)


def calculate_new_coordinates(coord, dist, alpha):
    dx = float(dist) * math.sin(alpha)
    dy = float(dist) * math.cos(alpha)
    # coord[0] is the latitude and longitude for starting point
    new_lat = float(coord[0]["x"]) + (dy / RADIUS_EARTH) * (SEMI_C / math.pi)
    new_lon = float(coord[0]["y"]) + (
        (dx / RADIUS_EARTH) * (SEMI_C / math.pi) / math.cos(coord[0]["x"] * math.pi / SEMI_C)
    )
    return (new_lat, new_lon)

def generate_circle_points(lat, lon, radius, name):
    # generate points
    circle_lats, circle_lons = [], []
    circle_names = []
    for k in range(N):
        # compute
        angle = pi*2*k/N
        dx = radius*cos(angle)
        dy = radius*sin(angle)
        circle_lats.append(lat + (SEMI_C/pi)*(dy/RADIUS_EARTH))
        circle_lons.append(lon + (SEMI_C/pi)*(dx/RADIUS_EARTH)/cos(lat*pi/SEMI_C))
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

# save the file with geo data
def save_geo_data_output_csv_file(geo_data):
    filename = args.output_geo_csv_file
    if not filename.endswith(".csv"):
        filename = filename + ".csv"
    with open(filename, "w", newline="") as csv_geo_data:
        headers = ["ap_hash", "latitude", "longitude", "time", "val"]
        writer = csv.DictWriter(csv_geo_data, fieldnames=headers)
        writer.writeheader()
        writer.writerows(geo_data)

# Drawing sorrunding APs
def drawing_circles_aps(gdf, subsets, fig):
    for i, ap_draw in gdf.iterrows():
        # if i > 0:
        for j, sub in enumerate(subsets):
            row = sub.loc[(sub["AP hash"] == ap_draw["ap_hash"]) & (sub["Time from start (seconds)"] == ap_draw["time"])]
            
            # Draw circles for APs observed from this point 
            if not row.empty:
                for s, aps in sub.iterrows():
                    hover_data = f"AP: {aps["AP hash"]}\n Dist: {aps["Distance (meters)"]} m\n From: {row.iat[0,0]}"
                    # we do not want to draw a circle for the current point
                    if row.iat[0, 0] is not aps["AP hash"]:
                        (circle_lats, circle_lons, circle_names) = generate_circle_points(ap_draw.latitude, ap_draw.longitude, aps["Distance (meters)"], hover_data)
                        draw_circle(circle_lats, circle_lons, circle_names, fig)


def main():
    # get coordinates from command line argument
    coordinates = get_coordinates()
    # calculate the angle for direction
    angle = calculate_angle(coordinates)

    # where to store the processed geo data
    geo_data = []

    # Process the data from WiFi Map CSV file from FlipperZero
    df = pd.read_csv(args.csv_wifi_map, sep=";")

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

    if args.output_geo_csv_file is not None:
        save_geo_data_output_csv_file(geo_data)

    gdf = pd.DataFrame.from_dict(geo_data)

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

    if args.draw_circles:
        drawing_circles_aps(gdf, subsets, fig)
        
    fig.update_layout(
            map_style="carto-darkmatter-nolabels",
            showlegend=False,
    )

    fig.show()
    print("Process and drawing done, visit your default browser")


if __name__ == "__main__":
    main()

