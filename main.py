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

def getContours(img):
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    maxArea = 0
    biggest = np.array([])

    for cnt in contours:
        area = cv2.contourArea(cnt)

        if area > 5000:
            cv2.drawContours(frameCnt, cnt, -1, (255, 0, 0), 3)
            perimeter = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*perimeter, True)

            if area > maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area
    
    return biggest

# Warp the image and get a perspective transform on the biggest contour portion
def getWarp(img, biggest):
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0,0], [frameWidth, 0], [0, frameHeight], [frameWidth, frameHeight]])

    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img, matrix, (frameWidth, frameHeight))

    return imgOutput


while cv2.waitKey(1) != 27:     # press ESC to break out
    _, frame = src.read()
    frame = cv2.flip(frame, 1)      #flips the camera to work as a mirror
    frameCnt = frame.copy()         # a copy to draw contours onto

    frame_pre = preprocessImage(frame)
    biggest = getContours(frame_pre)

    frameWarped = getWarp(frame, biggest)

    cv2.imshow("Original", frameWarped)

src.release()
cv2.destroyAllWindows()
