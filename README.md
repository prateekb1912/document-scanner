# OpenCV Document Scanner

This is a simple OpenCV project which scans any document and crops it out from the rest of the background, sort of like in document scanning mobile apps. I have used the Oython programming language and 
the OpenCV 4.2 library to use different functions and classes to achieve the result.

## THE PROCESS

First of all, I used the IP Webcam Android app to allow using my phone camera to scan documents near me. If you want to know more about it, click below:

[IP Webcam for OpenCV Instructions](https://origin.geeksforgeeks.org/connect-your-android-phone-camera-to-opencv-python/)

Next, we apply some preprocessing steps for contours to be formed on the image:
1. Change the image to grayscale
2. Blur the image
3. Generate canny features from the image
4. Dilate the image to increase the edge thickness
5. Erode the image to make edges thinner (We use a combination of dilation and erosion to make the edges appear more lively)

After pre-processing, we find contours in the image and draw them onto the original one. Here, we check if the area of selection has 4 corners or not. If the area is found, we dispaly
the contours, else we continue finding it. 

The last step is to warp the image and apply perspective transform to close up on the contour which contains our dcoument. When the warped image is displayed on the screen, the program
will grab a screenshot and save the file in the main code folder.

## HOW TO USE

1. Setup IP Webcam on your phone and connect your PC.
2. Clone the repo
3. In the repo folder, run the ```main.py``` file.
4. Use your phone to point on any document (Take care of camera adjustments)


More features will be added soon.
