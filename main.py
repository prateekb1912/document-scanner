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

def preprocessImage(img):
    # converting to grayscale
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # blurring
    imgBlur = cv2.blur(imgGray, (5, 5), 1)
    # generate canny features
    imgCanny = cv2.Canny(imgBlur, 100, 150)

    #Next, we will pass the image through 2 passes of dilation & 1 pass of erosion
    #so as to make the edges more visible
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=2)
    imgEros = cv2.erode(imgDil, kernel, iterations=1)

    return imgEros


while cv2.waitKey(1) != 27:     # press ESC to break out
    _, frame = src.read()
    frame = cv2.flip(frame, 1)      #flips the camera to work as a mirror

    frame = preprocessImage(frame)
    cv2.imshow("Original", frame)

src.release()
cv2.destroyAllWindows()
