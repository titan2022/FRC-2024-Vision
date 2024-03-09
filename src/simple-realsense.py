from ultralytics import YOLO
import pyrealsense2 as rs
from PIL import Image
import numpy as np
import ultralytics
import math
import cv2
import vision_functions

model = YOLO("YOLOv8sNO.pt")

pipe = rs.pipeline()
aligner = rs.align(rs.stream.color)
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

profile = pipe.start(config)

while True:
    frames = pipe.wait_for_frames()
    #frames = aligner.process(frames)
    color_frame = frames.get_color_frame()
    depth_frame = frames.get_depth_frame()
    
    color_im = np.asanyarray(color_frame.get_data())
    processing_im = color_im.copy()
    #cv2.cvtColor(color_im, cv2.COLOR_RGB2BGR, color_im)
    depth_im = np.asanyarray(depth_frame.get_data())

    result = model.track(processing_im, persist=True)
    annot_frame = result[0].plot()

    # if (result.__len__() >= 1):
    #     #x1, y1, x2, y2 = (int, int, int, int)
    #     x1, y1, x2, y2 = result[0].boxes.xyxy[0] #.numpy()
        
    #     bounding_box = color_im[y1:y2, x1:x2]
    #     cv2.imshow("Target",bounding_box)

    cv2.imshow("Tracking",annot_frame) #[...,[2,1,0]])
    cv2.imshow("Depth", depth_im * 255)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cv2.destroyAllWindows()