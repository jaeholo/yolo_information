import os
import numpy as np
import torch
os.add_dll_directory("C:\\Program Files (x86)\\VTK\\bin")  # not sure why interpreter is not finding this
import cv2
from ultralytics import YOLO
from tqdm import tqdm
from detection import Point, point_in_polygon, get_middle_point
import datetime
import pandas as pd

start_stamp = 1701419937000
start_time = datetime.datetime(2023,12,1,16,38,57)
lane = []
car_types = []
appear_time = []
appear_stamp = []
lane1_frame = 0
lane2_frame = 0
lane3_frame = 0



'''
the idea is to get the ordinal number of current frame which we detect the car, and then add on the STARTTIME,
so that we can know the timestamp the selected frame

set a detecting-line in this video, once the middle point of box arrives on the line, we would collect the info of this box(type, lane),
the y-axis of bottom line of the detecting area is 850, so if point.y=850 and is in the detecting area, notes it down 
'''
#def get_detection_time()
if __name__ == '__main__':
    lane1 = [
        Point(795, 725),
        Point(1032, 725),
        Point(841, 850),
        Point(546, 850)
    ]
    lane2 = [
        Point(1032, 725),
        Point(1281, 725),
        Point(1147, 850),
        Point(841, 850)
    ]
    lane3 = [
        Point(1281, 725),
        Point(1535, 725),
        Point(1452, 850),
        Point(1147, 850)
    ]
    detect_area = [
        Point(795, 725),
        Point(1535, 725),
        Point(1452, 850),
        Point(546, 850)
    ]
    # Open the video
    cap = cv2.VideoCapture(r"F:\hightway_video\cut_video.mp4")
    model = YOLO(r"F:\Project\AI_Lane\yolov8m.pt")
    count = 0  # this variable is to let us know which frame is now
    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret:
            count += 1
            # Create a copy of the original frame to modify
            detection_frame = frame.copy()

            # Perform inference on the modified frame
            results = model(detection_frame, conf=0.4)

            # Retrieve the bounding boxes from the results
            bounding_boxes = results[0].boxes

            # Initialize counters for vehicles in each lane
            # vehicles_in_left_lane = 0
            # vehicles_in_right_lane = 0
            lane1_car = 'No car'
            lane2_car = 'No car'
            lane3_car = 'No car'

            # Loop through each bounding box to count vehicles in each lane
            for i in range(len(bounding_boxes)):
                boxes = results[0].boxes[i]
                cls_key = boxes.cls.item()
                cls_name = model.names[cls_key]
                middle_point = get_middle_point(boxes)
                if cls_key == 2.0:
                    car_type = 'Small Car'
                else:
                    car_type = "Big Car"
                # if point is in specific area and the time gap between the last first detection is more than 1s
                if point_in_polygon(middle_point, lane1) and (count-lane1_frame) > 25:
                    # lane1_car = car_type
                    lane1_car = cls_name
                    lane1_frame = count
                    seconds = round(count/25)
                    current_time = start_time + datetime.timedelta(0, round(seconds))
                    current_stamp = str(start_stamp + 40*count)
                    lane.append("Lane 1")
                    car_types.append(cls_name)
                    appear_time.append(current_time)
                    appear_stamp.append(current_stamp)
                if point_in_polygon(middle_point, lane2) and (count-lane2_frame) > 25:
                    # lane2_car = car_type
                    lane2_car = cls_name
                    lane2_frame = count
                    seconds = round(count / 25)
                    current_time = start_time + datetime.timedelta(0, round(seconds))
                    current_stamp = str(start_stamp + 40 * count)
                    lane.append("Lane 2")
                    car_types.append(cls_name)
                    appear_time.append(current_time)
                    appear_stamp.append(current_stamp)
                if point_in_polygon(middle_point, lane3) and (count-lane3_frame) > 25:
                    # lane3_car = car_type
                    lane3_car = cls_name
                    lane3_frame = count
                    seconds = round(count / 25)
                    current_time = start_time + datetime.timedelta(0, round(seconds))
                    current_stamp = str(start_stamp + 40 * count)
                    lane.append("Lane 3")
                    car_types.append(cls_name)
                    appear_time.append(current_time)
                    appear_stamp.append(current_stamp)


        else:
            break

    df = pd.DataFrame({
        'lane': lane,
        'car_types': car_types,
        'appear_time': appear_time,
        'appear_stamp': appear_stamp
    })
    df.to_excel('C:/Users/hp/Desktop/detection.xlsx')