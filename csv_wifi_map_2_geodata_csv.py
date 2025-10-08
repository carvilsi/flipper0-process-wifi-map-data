# This script generates a geospatial CSV data

import csv
import sys
import math
import matplotlib.pyplot as plt

RADIUS_EARTH = 6378.137 * 1000

def calculate_angle(coord):
   m = (coord[1]["y"] - coord[0]["y"]) / (coord[1]["x"] - coord[0]["x"]) 
   alpha = math.atan(m)
   return alpha

def get_coordinates():
    origin_coords = sys.argv[2].split(",")
    origin_coord = {
            "x": float(origin_coords[0]),
            "y": float(origin_coords[1])
            }
    end_coords = sys.argv[3].split(",")
    end_coord = {
            "x": float(end_coords[0]),
            "y": float(end_coords[1])
            }
    return (origin_coord, end_coord)

def calculate_new_latitude(coord, dist, alpha):
    dx = float(dist) * math.sin(alpha)
    dy = float(dist) * math.cos(alpha)
    new_lat = float(coord["x"]) + (dy / RADIUS_EARTH) * (180 / math.pi)
    new_lon = float(coord["y"]) + ((dx / RADIUS_EARTH) * (180 / math.pi) / math.cos(coord["x"] * math.pi / 180))
    return (new_lat, new_lon)

## MAIN ##

if len(sys.argv) != 4:
    raise Exception("""
    You must provide a FlipperZero WiFi Map csv file and
    start and end maps coordinates""")

coordinates = get_coordinates()
angle = calculate_angle(coordinates)

geo_data = []

with open(sys.argv[1]) as file_obj:
    reader = csv.DictReader(file_obj, delimiter=";")

    time = None
    time_arr = []
    dist_arr = []
    ap_name_arr = []
    closer = 0

    for row in reader:
        ap_hash = row["AP hash"]
        distance = row["Distance (meters)"]
        ap_auth_mode = row["AP auth mode"]
        time = row["Time from start (seconds)"]

        time_arr.append(int(time))
        dist_arr.append(float(distance))
        ap_name_arr.append(ap_hash[5:])
        closer = float(distance)

    
