# import the necessary packages
import numpy as np
#import argparse
import cv2

if __name__ == '__main__':

    try:
        fn = sys.argv[1]
    except:
        fn = 0

    def nothing(*arg):
        pass

    # open capture
    cap = cv2.VideoCapture(0)

    # Presets  in Class    at home
    iLowH = 0    #0          0
    iHighH = 9   #179        9
    
    iLowS = 111  #191        111
    iHighS = 209 #255        209

    iLowV = 89   #4          89
    iHighV = 255 #150        255
    
    # keep looping
    while True:
        
        # grab the current frame
        (grabbed, frame) = cap.read()

        # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # define range of blue color in HSV
        lower_bound = np.array([ iLowH,  iLowS,  iLowV])
        upper_bound = np.array([iHighH, iHighS, iHighV])
 
        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
 
        # only proceed if at least one contour was found
        if len(cnts) > 0:
	    # find the largest contour in the mask, then use
	    # it to compute the minimum enclosing circle and
	    # centroid
	    c = max(cnts, key=cv2.contourArea)
	    ((x, y), radius) = cv2.minEnclosingCircle(c)
	    M = cv2.moments(c)
	    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            print('x : {0}, y : {1}').format(int(x - 320), int(y - 240))
            
	    # only proceed if the radius meets a minimum size
	    if radius > 10:
	        # draw the circle and centroid on the frame,
                # then update the list of tracked points
	        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
	        cv2.circle(frame, center, 5, (0, 0, 255), -1)
 
	# show the frame to our screen
	cv2.imshow("Frame", frame)
        cv2.imshow("Mask", mask)
 
	# exit statement
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
 
    # cleanup the camera and close any open windows
    cap.release()
    cv2.destroyAllWindows()
