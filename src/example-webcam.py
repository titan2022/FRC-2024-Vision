from ultralytics import YOLO
import pyrealsense2 as rs
from PIL import Image
import numpy as np
import ultralytics
import math
import cv2
import vision_functions

# Disable this unless Titan-Processing is built in ../Titan-Processing
ENABLE_TRBNETWORKING = True
if ENABLE_TRBNETWORKING:
    import pathlib
    import TRBNetworking

model = YOLO("YOLOv8sNO.pt")

cap = cv2.VideoCapture(0)

if ENABLE_TRBNETWORKING:
    libTitanProcessing = TRBNetworking.load_lib(pathlib.Path(__file__).parent.resolve() / ".." / ".." / "Titan-Processing" / "lib" / "libTitanProcessing.so")
    roboRIO = TRBNetworking.Client(libTitanProcessing, b"127.0.0.1", 5800)

while cap.isOpened():
    success, frame = cap.read()
    assert success

    res = model.track(frame, persist=True, conf=0.4)
    firstResult: ultralytics.engine.results.Results = res[0]
    annotatedFrame = firstResult.plot()
    boxes = firstResult.boxes.xyxy

    for x1, y1, x2, y2 in boxes:
        print(type(x1))
        print(((x1, y1), (x2, y2)))
        center = (int((x1.item() + x2.item())/2), int((y1.item() + y2.item())/2))
        print(center)
        cv2.circle(annotatedFrame, center, 7, (255, 0, 0), cv2.FILLED) # Show circle
        if ENABLE_TRBNETWORKING:
            # FIXME: We need to figure out a way to group these points by which frame they're in,
            #        so that the roboRIO doesn't think that there are two notes that are a few meters away
            roboRIO.sendVector(b"position", TRBNetworking.Vector3D(center[0], center[1], 0))

    cv2.imshow("Tracking", annotatedFrame)

    # Quit if Q or ESC is pressed
    keypress = cv2.waitKey(1)
    if keypress == ord('q') or keypress == 27:
        break

cap.release()
cv2.destroyAllWindows()