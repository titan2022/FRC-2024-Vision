from ultralytics import YOLO
import pyrealsense2 as rs
from PIL import Image
import numpy as np
import ultralytics
import math
import cv2
import vision_functions

model = YOLO("YOLOv8sNO.pt")

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    assert success

    res = model.track(frame, persist=True)
    annot_frame = res[0].plot()

    cv2.imshow("Tracking", annot_frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()