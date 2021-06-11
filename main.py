# Importing necessary libraries
import cv2
import numpy as np
import requests
import imutils

# Setting up IP webcam to connect to an Android phone 
url = 'http://192.168.1.104:8080/shot.jpg'
frameWidth = 1280
frameHeight = 960

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
    biggest = reorder(biggest)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0,0], [frameWidth, 0], [0, frameHeight], [frameWidth, frameHeight]])

    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img, matrix, (frameWidth, frameHeight))

    return imgOutput

# Reorders the warp points 
def reorder(points):
    points = points.reshape((4, 2))
    newPoints = np.zeros((4, 1, 2), np.int32)

    sum = points.sum(1)
    diff = np.diff(points, axis=1)

    newPoints[0] = points[np.argmin(sum)]
    newPoints[1] = points[np.argmin(diff)]
    newPoints[2] = points[np.argmax(diff)]
    newPoints[3] = points[np.argmax(sum)]

    return newPoints



while cv2.waitKey(1) != 27:     # press ESC to break out
    img_resp = requests.get(url, verify=False)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    frame = cv2.imdecode(img_arr, -1)
    frame = imutils.resize(frame, width=frameWidth, height=frameHeight)

    frameCnt = frame.copy()         # a copy to draw contours onto
    frame_pre = preprocessImage(frame)
    biggest = getContours(frame_pre)

    frameWarped = frameCnt

    if(biggest.shape != (0,)):
        frameWarped = getWarp(frame, biggest)
        cv2.imwrite('scanned.jpg', frameWarped)

    cv2.imshow("Original", frameWarped)

cv2.destroyAllWindows()
