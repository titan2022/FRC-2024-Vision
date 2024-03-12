from ultralytics import YOLO
import pyrealsense2 as rs
from PIL import Image
import numpy as np
import ultralytics
import torch
import math
import cv2 as cv
import vision_functions as vf

# Disable this unless Titan-Processing is built in ../Titan-Processing
ENABLE_TRBNETWORKING = False
if ENABLE_TRBNETWORKING:
    import pathlib
    import TRBNetworking

ENABLE_IMSHOW = False

# model = YOLO("YOLOv8sNO.pt") # Small model
model = YOLO("../yolov8n-note-only.pt") # Nano model

# # D435
# HFOV = 90
# VFOV = 64

# D455
HFOV = 90
VFOV = 64

pipe = rs.pipeline()
aligner = rs.align(rs.stream.color)
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

profile = pipe.start(config)

sensor = pipe.get_active_profile().get_device().first_depth_sensor()
sensor.set_option(rs.option.depth_units, 0.0001) # Set units to 0.0001 m = 0.1 mm = 100 µm

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
    #cv.cvtColor(color_im, cv.COLOR_RGB2BGR, color_im)
    depth_im = np.asanyarray(depth_frame.get_data())

    results = model.track(processing_im, persist=True, classes=["note"])
    firstResult: ultralytics.engine.results.Results = results[0]
    if ENABLE_IMSHOW:
        annotatedFrame = firstResult.plot()

    # boxes = firstResult.boxes.xyxy
    boxes: torch.Tensor = firstResult.boxes.xyxy
    # print(type(boxes))
    if boxes.numel() > 0:
        x1, x2, y1, y2 = 0, 0, 0, 0
        def key(box):
            x1, y1, x2, y2 = box
            return (x2-x1)**2 + (y2-y1)**2
        largestBox = max(boxes, key=key)
    else:
        largestBox = None

    hsv_mask = color_im
    mask = color_im

    # for x1, y1, x2, y2 in boxes:
    if largestBox is not None:
        x1, y1, x2, y2 = largestBox
        # print(type(x1))
        # print(((x1, y1), (x2, y2)))
        center_x = int((x1.item() + x2.item())/2)
        center_y = int((y1.item() + y2.item())/2)
        if ENABLE_IMSHOW:
            center = (center_x, center_y)
            # print(center)
            cv.circle(annotatedFrame, center, 7, (255, 0, 0), cv.FILLED) # Show circle
        # Let's do some depth stuff!
        hsv_frame = cv.cvtColor(color_im, cv.COLOR_BGR2HSV)
        #             HUE     SATURAT VALUE
        thresholds = [  0, 20, 90,255, 30,255]
        bb_mask = np.zeros(hsv_frame.shape[:2], dtype=np.uint8)
        cv.rectangle(bb_mask, (int(x1), int(y1)), (int(x2), int(y2)), 255, -1)
        hsv_mask = vf.hsv_filter(hsv_frame, thresholds)
        nonzero_mask = cv.inRange(depth_im, np.array([1]), np.array([65534]))
        mask = cv.bitwise_and(hsv_mask, nonzero_mask, mask=bb_mask)
        # depth = cv.mean(depth_im, hsv_mask)[0]
        note_z = cv.mean(depth_im, mask)[0]
        # print(f"Depth: {depth} | Sparse: {note_z}")
        

        if ENABLE_TRBNETWORKING:
            # FIXME: We need to calculate the position of the note on the field.
            roboRIO.sendVector(b"note", TRBNetworking.Vector3D(center[0], center[1], 0))

    if ENABLE_IMSHOW:
        # print(f"Mask: {mask}")
        cv.imshow("HSV Mask", hsv_mask)
        cv.imshow("Mask", mask)
        cv.imshow("Tracking", annotatedFrame)
        cv.imshow("Depth", depth_im * 10)

        # Quit if Q or ESC is pressed
        keypress = cv.waitKey(1)
        if keypress == ord('q') or keypress == 27:
            break

if ENABLE_IMSHOW:
    # cap.release()
    cv.destroyAllWindows()