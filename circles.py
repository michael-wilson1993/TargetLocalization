# import the necessary packages
from collections import deque
import numpy as np
import argparse
import cv2


if __name__ == '__main__':

    try:
        fn = sys.argv[1]
    except:
        fn = 0

    def nothing(*arg):
        pass

    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help="path to the (optional) video file")
    ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
    args = vars(ap.parse_args())


    
    # open capture
    cap = cv2.VideoCapture(0)

    # Presets  School1   School2     Home
    iLowH = 0     #0         0         0
    iHighH = 10   #179       10        9
    
    iLowS = 100   #191      100       111
    iHighS = 255  #255      255       209

    iLowV = 100   #4        100        89
    iHighV = 255  #150      255        255
    
    # Generate Sliders
    cv2.namedWindow('Control')
    
    cv2.createTrackbar( 'LowH', 'Control',  iLowH, 179, nothing)
    cv2.createTrackbar('HighH', 'Control', iHighH, 179, nothing)

    cv2.createTrackbar( 'LowS', 'Control',  iLowS, 255, nothing)
    cv2.createTrackbar('HighS', 'Control', iHighS, 255, nothing)

    cv2.createTrackbar( 'LowV', 'Control',  iLowV, 255, nothing)
    cv2.createTrackbar('HighV', 'Control', iHighV, 255, nothing)

    # list tracking pts
    pts = deque(maxlen=args["buffer"])
 

    # keep looping
    while True:
        
        # grab the current frame
        (grabbed, frame) = cap.read()

        # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Get Slider val
        iLowH = cv2.getTrackbarPos('LowH', 'Control')
        iHighH = cv2.getTrackbarPos('HighH', 'Control')
        
        iLowS = cv2.getTrackbarPos('LowS', 'Control')
        iHighS = cv2.getTrackbarPos('HighS', 'Control')

        iLowV = cv2.getTrackbarPos('LowV', 'Control')
        iHighV = cv2.getTrackbarPos('HighV', 'Control')

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
 
	    # only proceed if the radius meets a minimum size
	    if radius > 5 and radius < 50:
                # find x y coor and normalize
                print('x : {0}, y : {1}').format(int(x - 320), int(y - 240))
                
	        # draw the circle and centroid on the frame,
                # then update the list of tracked points
	        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
	        cv2.circle(frame, center, 5, (0, 0, 255), -1)
         
	# update the points queue
	pts.appendleft(center)

        # loop over the set of tracked points
	for i in xrange(1, len(pts)):
            # if either of the tracked points are None, ignore
	    # them
	    if pts[i - 1] is None or pts[i] is None:
                continue
 
            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
	    cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
 
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
