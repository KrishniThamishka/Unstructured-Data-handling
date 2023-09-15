import cv2 as cv
import numpy as np
from os.path import exists
import pandas as pd

file_prefix = "resources/subtitle/output1"
waypoint_srt_records =pd.read_csv(file_prefix + '.csv')

window_name = 'Processing'
file_name = "resources/subtitle/DJI_20230124113730_0001_W_Waypoint1.mp4"
cv.namedWindow(window_name, cv.WINDOW_NORMAL)

source = cv.VideoCapture(file_name)
framespersecond = float(source.get(cv.CAP_PROP_FPS))
success, image = source.read()
if not success:
    print("Failed to read video frame from file")
    exit()
height, width, lyers = image.shape
out = cv.VideoWriter(file_prefix + "_processed.mp4",
                    cv.VideoWriter_fourcc(*'mp4v'),
                    framespersecond, (width, height))
video_frame_count = 1
alpha = 0.7

while success and (cv.waitKey(1) & 0xFF != ord('q')) :
    frame_index = int(video_frame_count /  framespersecond)
    map_file = 'resources/map' + str(frame_index) + '.png'
    overlay = image.copy()
  
    lat = waypoint_srt_records['latitude'][frame_index]
    lon = waypoint_srt_records['Longitude'][frame_index]
    alt = waypoint_srt_records['Altitude'][frame_index]
    speed = waypoint_srt_records['Speed'][frame_index]
    distance = waypoint_srt_records['Distance'][frame_index]
    cv.putText(overlay, f'Latitude: {lat}', (1500, height - 100),
               cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv.putText(overlay, f'Longitude: {lon}', (1500, height - 70),
               cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv.putText(overlay, f'Altitude: {alt}', (1500, height - 40),
               cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv.putText(overlay, f'Speed: {speed} km/h', (800, height - 70),
               cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv.putText(overlay, f'Distance: {distance} km', (800, height - 40),
               cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    results = cv.addWeighted(overlay, alpha, image, 1-alpha, 0)
    if exists(map_file):
        map= cv.imread(map_file, results)
        results[300:500, height-100:height-10] = map[0:300, 0:400]
        
    out.write(results)
    cv.imshow(window_name,results)
    success, image = source.read()
    if video_frame_count % 30 == 0:
        #print("working...")
        video_frame_count += 1
    
source.release()
out.release()
cv.destroyAllWindows()
print('completed')