import argparse
import json
import csv
import math
from requests import get
from math import cos, asin, sqrt
import requests

parser = argparse.ArgumentParser()
parser.add_argument("baseURL", help="display given URL")
parser.add_argument("command", help="display given command")
parser.add_argument('parameter', nargs='*', default=[0, 0], help="display parameter", type=float)
args = parser.parse_args()
print("Command = " + args.command)
if args.parameter != [0, 0]:
    print("Parameters = " + str(args.parameter))
else:
    print("Parameters = none")

station_infoURL = args.baseURL + 'station_information.json'
station_statusURL = args.baseURL + 'station_status.json'

# dict for station info------------------------------------------------------
station_info_response = get(station_infoURL)
station_info_response_dict = json.loads(station_info_response.text)
station_info_dict = station_info_response_dict['data']['stations']

# dict for station status----------------------------------------------------
station_status_response = get(station_statusURL)
station_status_response_dict = json.loads(station_status_response.text)
station_status_dict = station_status_response_dict['data']['stations']

# task1 --------------------------------------------------------------------------
if args.command == "total_bikes":
    bike_count = 0
    for row in station_status_dict:
        bike_count = bike_count + int(row['num_bikes_available'])

    print("output = " + str(bike_count))

# task2 ----------------------------------------------------------------------------
elif args.command == "total_docks":
    docks_count = 0
    for row in station_status_dict:
        docks_count = docks_count + int(row['num_docks_available'])

    print("output = " + str(docks_count))

# task3 -------------------------------------------------------------------------------------------
elif args.command == "percent_avail":
    num_bikes_available = 0
    num_docks_available = 0
    percentage = 0
    stationID = int(args.parameter[0])
    for row in station_status_dict:
        if row['station_id'] == str(stationID):
            num_docks_available = num_docks_available + int(row['num_docks_available'])
            num_bikes_available = num_bikes_available + int(row['num_bikes_available'])

    percentage = math.floor(num_docks_available / (num_bikes_available + num_docks_available) * 100)
    print(str(percentage) + '%')

# task4 --------------------------------------------------------------------------------------------------------
elif args.command == "closest_stations":

    def distance(lat1, lon1, lat2, lon2):
        p = 0.017453292519943295
        a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
        return 12742 * asin(sqrt(a))

    minimum_dist = {}
    latitude = args.parameter[0]
    longitude = args.parameter[1]
    dist1 = 100000.0
    dist2 = 100000.0
    dist3 = 100000.0
    station1 = ' '
    station2 = ' '
    station3 = ' '

    for row in station_info_dict:
        dist_diff = distance(row['lat'], row['lon'], latitude, longitude)
        minimum_dist[row['station_id']] = dist_diff

    for candidate in minimum_dist:
        if dist1 >= minimum_dist[candidate]:
            dist1 = minimum_dist[candidate]
            station1 = candidate

    for candidate in minimum_dist:
        if (dist2 >= minimum_dist[candidate]) & (candidate != station1):
            dist2 = minimum_dist[candidate]
            station2 = candidate

    for candidate in minimum_dist:
        if (dist3 >= minimum_dist[candidate]) & (candidate != station1) & (candidate != station2):
            dist3 = minimum_dist[candidate]
            station3 = candidate

    print('Output: ')
    for row in station_info_dict:
        if row['station_id'] == station1:
            print(str(station1) + ', ' + str(row['name']))

    for row in station_info_dict:
        if row['station_id'] == station2:
            print(str(station2) + ', ' + str(row['name']))

    for row in station_info_dict:
        if row['station_id'] == station3:
            print(str(station3) + ', ' + str(row['name']))

# task 5---------------------------------------------------------------------------------------------------------------------------------
elif args.command == "closest_bike":

    def distance(lat1, lon1, lat2, lon2):
        p = 0.017453292519943295
        a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
        return 12742 * asin(sqrt(a))

    minimum_dist = {}
    latitude = args.parameter[0]
    longitude = args.parameter[1]
    dist1 = 100000.0
    station1 = ' '

    for row in station_info_dict:
        dist_diff = distance(row['lat'], row['lon'], latitude, longitude)
        minimum_dist[row['station_id']] = dist_diff

    for candidate in minimum_dist:
        for row in station_status_dict:
            if ((dist1 >= minimum_dist[candidate]) & (row['num_bikes_available'] != 0) & (row['station_id'] == candidate)):
                #print(row['num_bikes_available'])
                dist1 = minimum_dist[candidate]
                station1 = candidate
                #print(station1)

    for row in station_info_dict:
        if row['station_id'] == station1:
            print('Output: ' + str(station1) + ', ' + str(row['name']))


