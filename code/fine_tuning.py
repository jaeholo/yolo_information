import os
import numpy as np
import torch
os.add_dll_directory("C:\\Program Files (x86)\\VTK\\bin")  # not sure why interpreter is not finding this
import cv2
from ultralytics import YOLO
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"


if __name__ == '__main__':
    model = YOLO('yolov8m.pt')
    dataset_path = r"F:\dataset\BITVehicle_Dataset"
    yaml_file_path = os.path.join(dataset_path, 'data.yaml')
    results = model.train(
        data=yaml_file_path,  # Path to the dataset configuration file
        epochs=50,  # Number of epochs to train for
        imgsz=640,  # Size of input images as integer
        device=0,  # Device to run on, i.e. cuda device=0
        patience=50,  # Epochs to wait for no observable improvement for early stopping of training
        batch=32,  # Number of images per batch
        optimizer='auto',  # Optimizer to use, choices=[SGD, Adam, Adamax, AdamW, NAdam, RAdam, RMSProp, auto]
        lr0=0.0001,  # Initial learning rate
        lrf=0.1,  # Final learning rate (lr0 * lrf)
        dropout=0.1,  # Use dropout regularization
        seed=0  # Random seed for reproducibility
    )