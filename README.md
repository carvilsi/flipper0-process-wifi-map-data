# flipper0-process-wifi-map-data

<div align="center">
    <p>Scripts to process FlipperZero WiFi Map data to geolocate APs from wardriving sessions</p>
    <p>
        <img src="https://github.com/carvilsi/flipper0-process-wifi-map-data/blob/main/.github/images/overview_wifi_map_aps_radius.png" alt="overview_wifi_map_aps_radius" >
    </p>
</div>

---

In order to get the data you'll need the app [FlipperZero WiFi-Map](https://github.com/carvilsi/flipper0-wifi-map) and it's [ESP32 companion](https://github.com/carvilsi/esp32-wifi-map)

## Run


```
usage: csv_wifi_map_2_geodata_csv.py [-h] [-dc] [-o OUTPUT_GEO_CSV_FILE] csv_wifi_map start_coordinates end_coordinates

Process the colected APs data on FlipperZero and draws the the points on OpenStreetMap map e.g. ./csv_wifi_map_2_geodata_csv.py path/to/csv '39.635191,-0.239454' '39.635192,-0.239455'

positional arguments:
  csv_wifi_map          path to the csv WiFi-Map file from FlipperZero
  start_coordinates     The start cordinates point, 'latitude,longitde' you can get this on https://www.openstreetmap.org using
                        'Center Map here' and getting it from url; e.g. '39.635191,-0.239454'
  end_coordinates       The end cordinates point, 'latitude,longitde' you can get this on https://www.openstreetmap.org using 'Center
                        Map here' and getting it from url; e.g. '39.635192,-0.239455'

options:
  -h, --help            show this help message and exit
  -dc, --draw_circles   If set will draw circles with estimated distance to the AP
  -o, --output_geo_csv_file OUTPUT_GEO_CSV_FILE
                        Saves the processed data on CSV file
```

### Examples

#### Plot APs relevant points

Plot the geolocated warwalking colected data:

`$ ./csv_wifi_map_2_geodata_csv.py path/to/csv '39.635191,-0.239454' '39.635192,-0.239455'`

<div align="center">
    <p>
        <img src="https://github.com/carvilsi/flipper0-process-wifi-map-data/blob/main/.github/images/detail_points_wifi_map.png" alt="detail_points_wifi_map" >
    </p>
    <p>
        <img src="https://github.com/carvilsi/flipper0-process-wifi-map-data/blob/main/.github/images/points_wifi_map.png" alt="points_wifi_map" >
    </p>
</div>

#### Plot APs relevant points and circles with estimated distance for retrieved APs


Plot the geolocated warwalking colected data and sorounding APs:

`$ ./csv_wifi_map_2_geodata_csv.py path/to/csv --draw_circles '39.635191,-0.239454' '39.635192,-0.239455'`

<div align="center">
    <p>
        <img src="https://github.com/carvilsi/flipper0-process-wifi-map-data/blob/main/.github/images/detail_wifi_map_aps_radius.png" alt="detail_wifi_map" >
    </p>
</div>


#### Plot APs relevant points and circles with estimated distance for retrieved APs

Plot and save processed data to CSV file:

`$ ./csv_wifi_map_2_geodata_csv.py path/to/csv --draw_circles '39.635191,-0.239454' '39.635192,-0.239455' -o outpu_processed.csv`

## Jupiter Notebooks

Small notebooks to play around with collected data.

### Analyze

- [notebook](https://github.com/carvilsi/flipper0-process-wifi-map-data/blob/main/jupyter-notebooks/WiFi_Map_analyze.ipynb)

### Process

To try things related with processing the collected data from warwalking

- [notebook](https://github.com/carvilsi/flipper0-process-wifi-map-data/blob/main/jupyter-notebooks/WiFi_maps_process.ipynb)

## Caveats

The locations are not so accurate when the walk is not a straight line.

## TODOs

- [ ] correct with end coordinate
- [x] add auth mode to generated geodata (for viz)
- [ ] work on export file to do navigation on FlipperZero side 
- [ ] try to solve possitions when not walking straight
