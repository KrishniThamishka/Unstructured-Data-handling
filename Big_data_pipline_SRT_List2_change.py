import pandas as pd
import re
import cv2 as cv
import numpy as np
from math import sin, cos, sqrt, atan2, radians
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Process SRT file and output data in JSON or CSV format')
parser.add_argument('--format', choices=['csv', 'json'], default='csv', help='d2_SRT_List2_change.py')
parser.add_argument('filename', help='d2_SRT_List2_change.py')
args = parser.parse_args()

file_name = 'resources/subtitle/DJI_20230124113730_0001_W_Waypoint1.SRT'

frame_integer_re = '^[0-9]+$'

with open(file_name) as f:
    lines = [line.rstrip('\n') for line in f]

#for line in lines:  
# print(line)

df = pd.DataFrame(columns=['Frame No', 'Start','End', 'latitude', 'Longitude', 'Altitude', 'Speed', 'Distance'])

def distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6731.0
    lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

for index in range(len(lines)):
    line_str = lines[index] 
    match = re.search(frame_integer_re, line_str)
    #if re.search(frame_integer_re, line_str) != None:
    if match != None:
        sequence_number = line_str
        if sequence_number != '0':
             #print(sequence_number)
            start = lines[index + 1].strip()[3:12]
            #print(satrt_time)
            end = lines[index + 1].strip()[20:29]
            #print(end_time)
            lat = lines[index + 5].strip()[11:19]
            #print(lat)
            lng = lines[index + 5].strip()[33:42]
            #print(lng)
            alt = lines[index + 5].strip()[-8:-1]
            #print(alt)
            #index += 12
            total_speed = np.sqrt((float(lines[index + 6].strip()[15:19]))**2 + (float(lines[index + 6].strip()[34:38]))**2 + (float(lines[index + 6].strip()[-4:-1]))**2)
            #print(total_speed)
            
            # Calculate distance from previous latitude and longitude
            if len(df) > 0:
                prev_lat = df.iloc[-1]['latitude']
                prev_lng = df.iloc[-1]['Longitude']
                dist = distance(prev_lat, prev_lng, lat, lng)
            else:
                dist = 0.0

            row = {
                'Frame No': sequence_number,
                'Start': start,
                'End' : end,
                'latitude': lat,
                'Longitude': lng,
                'Altitude': alt,
                'Speed': total_speed,
                'Distance': dist
            }

            df.loc[len(df)] = row
            index += 12

#print(df)
if args.format == 'csv':
    df.to_csv('resources/subtitle/output1.csv', index=False)
    print('Data written to output1.csv')
elif args.format == 'json':
    df.to_json('resources/subtitle/output1.json', orient='records')
    print('Data written to output1.json')

#python code for script
#/usr/local/bin/python3 "/Users/user/Desktop/4th Year_I/DSC4013 - Big Data Analytics II (3)/Lecture2/d2_SRT_List2.py" --format csv resources/subtitle/DJI_20230124113730_0001_W_Waypoint1.SRT



