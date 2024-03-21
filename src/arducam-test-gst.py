import cv2

cameraName = "usb-Arducam_Technology_Co.__Ltd._Arducam_OV9782_USB_Camera_UC852-video-index0"

cap = cv2.VideoCapture(f"v4l2src device=/dev/v4l/by-id/{cameraName} ! "
                        "videorate ! videoconvert ! videoscale !"
                        "video/x-raw, format=BGR, width=640, height=480, pixel-aspect-ratio=1/1, framerate=30/1 ! "
                        "decodebin ! videoconvert ! appsink")

if not cap.isOpened():
    print("Cannot capture from camera. Exiting.")
    quit()

while True:
    success, frame = cap.read()
    #
    if success == False:
        break

    cv2.imshow("Frame from Arducam",frame)

    framerate = cap.get(cv2.CAP_PROP_FPS)
    print(f"Framerate: {framerate} frames/s")

    keypress = cv2.waitKey(1)
    ESCAPE = 27
    if keypress == ESCAPE:
        break

cap.release()
cv2.destroyAllWindows()