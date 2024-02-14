import numpy as np
import cv2 as cv
import pyrealsense2 as rs
import pynput.keyboard as keyboard
import time
import threading


#Variables for the threads
file = "data/test"
toRun = True
pause = False
pointOneX = 0
pointOneY = 0
pointTwoX = 0
pointTwoY = 0
color_frame = cv.Mat()
depth_frame = cv.Mat()

#Parameters
x_resolution = 640
y_resolution = 480
frame_rate = 30

def get_mouse_position(event,x,y,flags,param):
    if event == cv.EVENT_LBUTTONDBLCLK:
        if pause == False:
            pointOneX = x
            pointOneY = y
            pause = True
        elif pause == True:
            pointTwoX,pointTwoY = x,y
			#Save matrices
	

            pause = False
	
def on_press(key):
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k == 'n':
        toRun = False
        return False

config = rs.config()
config.enable_stream(rs.stream.depth, x_resolution, y_resolution, rs.format.any, frame_rate)
config.enable_stream(rs.stream.color, x_resolution, y_resolution, rs.format.any, frame_rate)
config.disable_stream(rs.stream.gyro)
config.disable_stream(rs.stream.accel)

cv.namedWindow("Current Frame")
cv.setMouseCallback("Current Frame", get_mouse_position)

listener = keyboard.Listener(on_press=on_press)
listener.start()  # start to listen on a separate thread

# Create a context object. This object owns the handles to all connected realsense devices
pipeline = rs.pipeline()
aligner = rs.align(rs.stream.depth)

# Start streaming
pipeline.start(config)

while toRun:
    frames = pipeline.wait_for_frames()
    frames = aligner.process(frames)
    
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()
    cv.cvtColor(color_frame, cv.COLOR_RGB2BGR, color_frame)
    cv.imshow("CurrentFrame", color_frame)
    cv.waitKey(1)
    while pause: 
        time.sleep(0.05)

# def on_press(key):
#     try:
#         k = key.char  # single-char keys
#     except:
#         k = key.name  # other keys
#     if k == 'y':  # keys of interest
#         toSave = True
#         print("Saving image")
#     elif k == 'n':
#         toRun = False
#         return False


# listener = keyboard.Listener(on_press=on_press)
# listener.start()  # start to listen on a separate thread

# try:
#     # Create a context object. This object owns the handles to all connected realsense devices
#     pipeline = rs.pipeline()
#     aligner = rs.align()

#     # Start streaming
#     pipeline.start(config)
#     cv.namedWindow("Current Frame")
#     cv.setMouseCallback("Current Frame", get_mouse_position)

#     while toRun:
#         # This call waits until a new coherent set of frames is available on a device
#         # Calls to get_frame_data(...) and get_frame_timestamp(...) on a device will return stable values until wait_for_frames(...) is called
#         frames = pipeline.wait_for_frames()
#         frames = aligner.process(frames)
        
#         depth_frame = frames.get_depth_frame()
#         color_frame = frames.get_color_frame()
#         cv.cvtColor(color_frame, cv.COLOR_RGB2BGR, color_frame)
#         cv.imshow("CurrentFrame", color_frame)
#         cv.waitKey(1)
    