import os
import numpy as np
import torch
os.add_dll_directory("C:\\Program Files (x86)\\VTK\\bin")  # not sure why interpreter is not finding this
import cv2
from ultralytics import YOLO
from detection import Point, point_in_polygon, get_middle_point



if __name__ == '__main__':
    # initialize the detecting field of each lane
    lane1 = [
        Point(1043, 600),
        Point(1224, 600),
        Point(841, 850),
        Point(546, 850)
    ]
    lane2 =[
        Point(1224, 600),
        Point(1415, 600),
        Point(1147, 850),
        Point(841, 850)
    ]
    lane3 = [
        Point(1415, 600),
        Point(1618, 600),
        Point(1452, 850),
        Point(1147, 850)
    ]

    # define the detection area
    vertices = np.array([(1043, 600), (1618, 600), (1452, 850), (546, 850)], dtype=np.int32)
    # Define the positions for the text annotations on the image
    text_lane1 = (10, 50)
    text_lane2 = (10, 100)
    text_lane3 = (10, 150)

    # Define font, scale, and colors for the annotations
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_color = (255, 255, 255)  # White color for text
    background_color = (255, 0, 0)  # Red background for text

    # Open the video
    cap = cv2.VideoCapture(r"F:\hightway_video\cut_video.mp4")

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('traffic_analysis_fine.avi', fourcc, 25.0, (int(cap.get(3)), int(cap.get(4))))
    model = YOLO(r"F:\Project\AI_Lane\runs\detect\train4\weights\best.pt")
    # Read until video is completed
    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret:
            # Create a copy of the original frame to modify
            detection_frame = frame.copy()

            # Perform inference on the modified frame
            results = model(detection_frame, conf=0.4)
            # processed_frame = results[0].plot(line_width=1)

            # Draw the quadrilaterals on the processed frame
            cv2.polylines(detection_frame, [vertices], isClosed=True, color=(0, 255, 0), thickness=2)

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
                if point_in_polygon(middle_point, lane1):
                    # lane1_car = car_type
                    lane1_car = cls_name
                if point_in_polygon(middle_point, lane2):
                    # lane2_car = car_type
                    lane2_car = cls_name
                if point_in_polygon(middle_point, lane3):
                    # lane3_car = car_type
                    lane3_car = cls_name
            # Write the processed frame to the output video
            cv2.putText(detection_frame, f'Lane1: {lane1_car} detected',
                                        text_lane1,
                                        font, font_scale, font_color, 2, cv2.LINE_AA)
            cv2.putText(detection_frame, f'Lane2: {lane2_car} detected',
                        text_lane2,
                        font, font_scale, font_color, 2, cv2.LINE_AA)
            cv2.putText(detection_frame, f'Lane3: {lane3_car} detected',
                        text_lane3,
                        font, font_scale, font_color, 2, cv2.LINE_AA)
            out.write(detection_frame)

            # Uncomment the following 3 lines if running this code on a local machine to view the real-time processing results
            # cv2.imshow('Real-time Analysis', processed_frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):  # Press Q on keyboard to exit the loop
            #     break
        else:
            break

    # Release the video capture and video write objects
    cap.release()
    out.release()