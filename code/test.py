import os
import numpy as np
import torch


os.add_dll_directory("C:\\Program Files (x86)\\VTK\\bin")  # not sure why interpreter is not finding this

import cv2


def extractImages(pathIn, pathOut):
    count = 0
    vidcap = cv2.VideoCapture(pathIn)
    success,image = vidcap.read()
    success = True
    while success:
        vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))    # added this line
        success,image = vidcap.read()
        print ('Read a new frame: ', success)
        cv2.imwrite( pathOut + "frame%d.jpg" % count, image)     # save frame as JPEG file
        count = count + 1
        break


if __name__ == '__main__':
    video_path = r"F:\hightway_video\cut_video.mp4"
    extractImages(video_path, 'F:/Project/AI_Lane/')
