# This script just draws the APs distance Vs time

import csv
import sys
import matplotlib.pyplot as plt

if len(sys.argv) == 1:
    raise Exception("You must provide a FlipperZero WiFi Map csv file")

with open(sys.argv[1]) as file_obj:
    reader = csv.DictReader(file_obj, delimiter=";")

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

    # draw something
    plt.xlabel("Time since ESP32 is connected to FlipperZero (s)")
    plt.ylabel("Distance to AP (m)")

    plt.plot(time_arr, dist_arr, ".")
    i = 0
    for x, y in zip(time_arr, dist_arr):
        plt.annotate(
            ap_name_arr[i],
            (x, y),
            textcoords="offset points",
            xytext=(0, 0),
            ha="right",
        )
        i += 1

    plt.show()
