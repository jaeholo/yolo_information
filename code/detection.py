import os
import numpy as np
import torch
os.add_dll_directory("C:\\Program Files (x86)\\VTK\\bin")  # not sure why interpreter is not finding this
import cv2
from ultralytics import YOLO

'''
how to define which lane the car is driving on 
resolution is 1920*1080
yolo output box type we choose xyxy here, which means top-left & bottom-right
'''


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def point_in_polygon(point, polygon):
    num_vertices = len(polygon)
    x, y = point.x, point.y
    inside = False

    # Store the first point in the polygon and initialize the second point
    p1 = polygon[0]

    # Loop through each edge in the polygon
    for i in range(1, num_vertices + 1):
        # Get the next point in the polygon
        p2 = polygon[i % num_vertices]

        # Check if the point is above the minimum y coordinate of the edge
        if y > min(p1.y, p2.y):
            # Check if the point is below the maximum y coordinate of the edge
            if y <= max(p1.y, p2.y):
                # Check if the point is to the left of the maximum x coordinate of the edge
                if x <= max(p1.x, p2.x):
                    # Calculate the x-intersection of the line connecting the point to the edge
                    x_intersection = (y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y) + p1.x

                    # Check if the point is on the same line as the edge or to the left of the x-intersection
                    if p1.x == p2.x or x <= x_intersection:
                        # Flip the inside flag
                        inside = not inside

        # Store the current point as the first point for the next iteration
        p1 = p2

    # Return the value of the inside flag
    return inside


def get_middle_point(boxes):
    x = boxes.xywh[0][0].item()
    y = boxes.xyxy[0][3].item()
    return Point(x, y)


def lane_judgement(result):
    object_num = len(result[0].boxes)
    for i in range(object_num):
        boxes = result[0].boxes[i]
        cls_key = boxes.cls.item()
        cls_name = dict[cls_key]
        middle_point = get_middle_point(boxes)
        if point_in_polygon(middle_point, lane1):
            print(f"Item {i} {cls_name} is inside the lane1")
        elif point_in_polygon(middle_point, lane2):
            print(f"Item {i} {cls_name} is inside the lane2")
        elif point_in_polygon(middle_point, lane3):
            print(f"Item {i} {cls_name} is inside the lane3")
        # else:
        #     print(f"Item {i} {cls_name} is not on the road")


if __name__ == '__main__':
    img_path = r"F:\hightway_video\cut_video.mp4"
    model = YOLO(r"F:\Project\AI_Lane\runs\detect\train8\weights\best.pt")
    result = model(img_path, save=True, conf=0.3)
    # window_name = 'Lane_test'
    # img = cv2.imread(img_path)
    # lane1 = [()]
    # img = cv2.line(img, (90, 1080), (1440, 400), (0, 255, 0), 1)
    # img = cv2.line(img, (490, 1080), (1530, 400), (0, 255, 0), 1)
    # img = cv2.line(img, (900, 1080), (1630, 400), (0, 255, 0), 1)
    # img = cv2.line(img, (1300, 1080), (1750, 400), (0, 255, 0), 1)
    # img = cv2.line(img, (0, 850), (1920,850), (0, 0, 255), 1)
    # img = cv2.line(img, (0, 600), (1920, 600), (0, 0, 255), 1)

    # Define 3 lanes' area

    # lane1 = [
    #     Point(1043, 600),
    #     Point(1224, 600),
    #     Point(841, 850),
    #     Point(546, 850)
    # ]
    # lane2 =[
    #     Point(1224, 600),
    #     Point(1415, 600),
    #     Point(1147, 850),
    #     Point(841, 850)
    # ]
    # lane3 = [
    #     Point(1415, 600),
    #     Point(1618, 600),
    #     Point(1452, 850),
    #     Point(1147, 850)
    # ]
    # # cv2.imwrite('F:/Project/AI_Lane/detection.jpg', img)


