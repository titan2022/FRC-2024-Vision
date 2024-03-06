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

    res = model.track(frame, persist=True, conf=0.4)
    firstResult: ultralytics.engine.results.Results = res[0]
    annot_frame = firstResult.plot()
    boxes = firstResult.boxes.xyxy

    for x1, y1, x2, y2 in boxes:
        print(type(x1))
        print(((x1, y1), (x2, y2)))
        center = (int((x1.item() + x2.item())/2), int((y1.item() + y2.item())/2))
        print(center)
        cv2.circle(frame, center, 7, (255, 0, 0), cv2.FILLED) # Show circle

    cv2.imshow("Tracking", annot_frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()