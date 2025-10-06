import sys
import os

if len(sys.argv) == 1:
    raise Exception("You must provide a FlipperZero WiFi Map csv file")

working_folder = "flpprzr_wfm_workspace" if len(sys.argv) == 2 else sys.argv[2]

if not os.path.exists(working_folder):
        os.makedirs(working_folder)

file_tmp = None

with open(sys.argv[1], "r") as file:
    for line in file:
        if line.startswith("#####"):
            data_date = line.split(" ")
            file_name = working_folder + "/" + data_date[1].replace(":", "_") + "-flpprzr_wfm.csv"
            print("Creating: " + file_name)
            file_tmp = open(file_name, "w")
            file_tmp.write("AP hash;Distance (meters);AP auth mode;Time from start (seconds)\n")
        else:
            file_tmp.write(line)

