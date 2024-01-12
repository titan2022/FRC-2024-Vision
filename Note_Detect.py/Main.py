import numpy as np
import cv2 as cv


#ITC = Image Testing Code


cap = cv.VideoCapture(0)
#cap = cv.imread('image1.png') # ITC


while cap.isOpened():
#while True:# ITC
  ret, frame = cap.read() #Get frame
  hsv_cap = cv.cvtColor(frame,cv.COLOR_BGR2HSV) 
  
  #hsv_cap = cv.cvtColor(cap,cv.COLOR_BGR2HSV) # ITC

  #Color Thresholds:
  lower_threshold = np.array([160,10,40])
  upper_threshold = np.array([180,60,100])
  
  #Create Mask
  mask = cv.inRange(hsv_cap, lower_threshold, upper_threshold)
  
  #Find Contours
  contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
 
  #Draw contours on original frame
  cv.drawContours(frame, contours, -1, (0,255,0),3)
  #cv.drawContours(cap, contours, -1, (0,255,0),3) # ITC
  cv.imshow('frame', frame) 
  if cv.waitKey(1) == ord('q'):
    break
  
  
cap.release()
cv.destroyAllWindows()
   