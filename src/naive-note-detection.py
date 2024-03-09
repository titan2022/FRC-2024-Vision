import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)
    
while cap.isOpened():
    # Get frame
    ret, frame = cap.read()
    
    # Convert to HSV (Hue Value Saturation)
    raw_image = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Color thresholds (HSV)
    lower_threshold = np.array([0, 90, 30])
    upper_threshold = np.array([20, 255, 255])

    # Create mask
    mask = cv.inRange(raw_image, lower_threshold, upper_threshold)

    # Get mean
    

    # Get contours
    contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    # Convert back to BGR, draw contours
    final_image = cv.cvtColor(raw_image, cv.COLOR_HSV2BGR)
    cv.drawContours(final_image, contours, -1, (0, 255, 0), 3)

    # new code here
    areas = [cv.contourArea(c) for c in contours]
    sorted_areas = np.sort(areas)

    if len(sorted_areas) >= 1:
        # Fit a circle on the biggest contour
        biggest_contour = contours[areas.index(sorted_areas[-1])]
        mu = cv.moments(biggest_contour)
        try:
            x, y = mu['m10']/mu['m00'], mu['m01']/mu['m00']
            center = (int(x), int(y))
            cv.circle(final_image, center, 7, (255, 0, 0), cv.FILLED) # Show circle
        except: pass
        # (x, y), radius = cv.minEnclosingCircle(biggest_contour)
        # center = (int(x), int(y))
        # radius = int(radius)
        # cv.circle(final_image, center, radius, (255, 0, 0), 2) # Show circle

        # # Calculate positions
        # f = 400 # Change to your focal point
        # D = 6
        # d = radius * 2

        # L = -1
        # if d != 0:
        #     L = (D * f) / d

        # print(L) # Actual distance to the circle in cm
        # pass

    # Show frame
    cv.imshow("Mask", mask)
    cv.imshow("Feed", final_image)

    # Quit if Q or ESC is pressed
    keypress = cv.waitKey(1)
    if keypress == ord('q') or keypress == 27:
        break

# Close window
cap.release()
cv.destroyAllWindows()