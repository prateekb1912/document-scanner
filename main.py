# Importing necessary libraries
import cv2
import numpy as np

# Setting up webcam
frameWidth = 640
frameHeight = 480

src = cv2.VideoCapture(0)

src.set(3, frameWidth)
src.set(4, frameHeight)
src.set(10, 130) 


while cv2.waitKey(1) != 27:     # press ESC to break out
    _, frame = src.read()
    frame = cv2.flip(frame, 1)      #flips the camera to work as a mirror
    cv2.imshow("Original", frame)

src.release()
cv2.destroyAllWindows()
