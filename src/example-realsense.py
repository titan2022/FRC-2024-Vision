from ultralytics import YOLO
import pyrealsense2 as rs
from PIL import Image
import numpy as np
import ultralytics
import torch
import math
import cv2
import vision_functions as vf

# Disable this unless Titan-Processing is built in ../Titan-Processing
ENABLE_TRBNETWORKING = False
if ENABLE_TRBNETWORKING:
    import pathlib
    import TRBNetworking

model = YOLO("YOLOv8sNO.pt")

pipe = rs.pipeline()
aligner = rs.align(rs.stream.color)
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

profile = pipe.start(config)

if ENABLE_TRBNETWORKING:
    libTitanProcessing = TRBNetworking.load_lib(pathlib.Path(__file__).parent.resolve() / ".." / ".." / "Titan-Processing" / "lib" / "libTitanProcessing.so")
    roboRIO = TRBNetworking.Client(libTitanProcessing, b"127.0.0.1", 5800)

while True:
    frames = pipe.wait_for_frames()
    frames = aligner.process(frames)
    color_frame = frames.get_color_frame()
    depth_frame = frames.get_depth_frame()
    
    color_im = np.asanyarray(color_frame.get_data())
    processing_im = color_im.copy()
    #cv2.cvtColor(color_im, cv2.COLOR_RGB2BGR, color_im)
    depth_im = np.asanyarray(depth_frame.get_data())

    results = model.track(processing_im, persist=True)
    firstResult: ultralytics.engine.results.Results = results[0]
    annotatedFrame = firstResult.plot()

    # boxes = firstResult.boxes.xyxy
    boxes: torch.Tensor = firstResult.boxes.xyxy
    print(type(boxes))
    if boxes.numel() > 0:
        x1, x2, y1, y2 = 0, 0, 0, 0
        def key(box):
            x1, y1, x2, y2 = box
            return (x2-x1)**2 + (y2-y1)**2
        largestBox = max(boxes, key=key)
    else:
        largestBox = None

    # for x1, y1, x2, y2 in boxes:
    if largestBox is not None:
        x1, y1, x2, y2 = largestBox
        print(type(x1))
        print(((x1, y1), (x2, y2)))
        center = (int((x1.item() + x2.item())/2), int((y1.item() + y2.item())/2))
        print(center)
        cv2.circle(annotatedFrame, center, 7, (255, 0, 0), cv2.FILLED) # Show circle
        # Let's do some depth stuff!
        

        if ENABLE_TRBNETWORKING:
            # FIXME: We need to calculate the position of the note on the field.
            roboRIO.sendVector(b"note", TRBNetworking.Vector3D(center[0], center[1], 0))

    cv2.imshow("Tracking", annotatedFrame)
    cv2.imshow("Depth", depth_im * 255)

    # Quit if Q or ESC is pressed
    keypress = cv2.waitKey(1)
    if keypress == ord('q') or keypress == 27:
        break

# cap.release()
cv2.destroyAllWindows()