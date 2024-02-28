import os
import numpy as np
import torch
os.add_dll_directory("C:\\Program Files (x86)\\VTK\\bin")  # not sure why interpreter is not finding this
import cv2
from ultralytics import YOLO
from tqdm import tqdm
from detection import Point, point_in_polygon

# def mask_img(img):


def extract_box(model, img, save_dir, current_frame):
    result = model(img, conf=0.6)
    for i in range(len(result[0].boxes)):
        box = result[0].boxes[i]
        x = box.xywh[0][0].item()
        y = box.xywh[0][1].item()
        center = Point(x, y)
        if box.cls.item() != 9.0 and point_in_polygon(center, bottom_triangle):
            x_min = int(box.xyxy[0][0].item())
            y_min = int(box.xyxy[0][1].item())
            x_max = int(box.xyxy[0][2].item())
            y_max = int(box.xyxy[0][3].item())
            crop_img = img[y_min:y_max, x_min:x_max]
            cv2.imwrite(save_dir + f"{current_frame}_{i}.jpg", crop_img)


def extract_frame(video_path):
    cap = cv2.VideoCapture(video_path)
    # frame_num = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # currently, the given video is not complete, missing some info about the video itself
    for current_frame in tqdm(range(0, 25500, 10)):
        cap.set(1, current_frame)
        ret, frame = cap.read()
        extract_box(model=model, img=frame, save_dir=save_dir, current_frame=current_frame)


if __name__ == '__main__':
    # model = YOLO(r"F:\Project\AI_Lane\runs\detect\train3\weights\best.pt")
    global bottom_triangle
    bottom_triangle = [
        Point(1920, 0),
        Point(1920, 1080),
        Point(0, 1080)
    ]
    video_path = r"F:\hightway_video\北绕城高速上行线K94+500_05B78760_1703983877_39.mp4"
    model = YOLO(r"F:\Project\AI_Lane\yolov8m.pt")
    save_dir = "C:/Users/hp/Desktop/saveimg/"
    extract_frame(video_path)



