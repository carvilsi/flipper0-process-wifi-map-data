# this script converts from NMEA GGA GPS output to
# map coordinates, the expected input is:
# GPGGA,095548.00,3939.67311,N,00013.63974,W,1,05,2.73,5.9,M,50.4,M,,*4A
import sys


def convert_latitude(loc_arr):
    gga_lat_arr = loc_arr[2].split(".")
    n_s = 1 if loc_arr[3] == "N" else -1
    lat_ll = gga_lat_arr[0][:2]
    lat_d = gga_lat_arr[0][2:] + "." + gga_lat_arr[1]
    lat = ((float(lat_d) / 60) + int(lat_ll)) * int(n_s)
    return lat


def convert_longitude(loc_arr):
    gga_lon_arr = loc_arr[4].split(".")
    e_w = 1 if loc_arr[5] == "E" else -1
    lon_ll = gga_lon_arr[0][:3]
    lon_d = gga_lon_arr[0][2:] + "." + gga_lon_arr[1]
    lon = ((float(lon_d) / 60) + int(lon_ll)) * int(e_w)
    return lon


# MAIN #

if len(sys.argv) == 1:
    raise Exception(
        "You must provide a GGA NEMA GPS, e.g: GPGGA,095548.00,3939.67311,N,00013.63974,W,1,05,2.73,5.9,M,50.4,M,,*4A"
    )

loc_arr = sys.argv[1].split(",")

lat_coords = convert_latitude(loc_arr)
lon_coords = convert_longitude(loc_arr)
print(str(lat_coords) + "," + str(lon_coords))
