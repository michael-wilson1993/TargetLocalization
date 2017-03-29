#include <iostream>
//#include <ros/ros.h>
#include <stdio.h>
#include <stdlib.h>
//#include <image_transport/image_transport.h>
//#include <cv_bridge/cv_bridge.h>
//#include <sensor_msgs/image_encodings.h>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

using namespace cv;
using namespace std;

int main( int argc, char** argv )
{
   // capture the video from webcam
   VideoCapture cap(1); 

   // if not success, exit program
   if ( !cap.isOpened() )  
   {
      cout << "Cannot open the web cam" << endl;
      return -1;
   }

   // create a window called "Control"
   //namedWindow("Control", CV_WINDOW_AUTOSIZE); 
   
   // (very accurate atleast for my light) 
   int iLowH = 23; // 0        0
   int iHighH = 38; // 9     179

   int iLowS = 77; // 111     191
   int iHighS = 154; // 209    255

   int iLowV = 145; // 89          4
   int iHighV = 175; // 255      150

   // Create trackbars in "Control" window
   //createTrackbar("LowH", "Control", &iLowH, 179); //Hue (0 - 179)
   //createTrackbar("HighH", "Control", &iHighH, 179);

   //createTrackbar("LowS", "Control", &iLowS, 255); //Saturation (0 - 255)
   //createTrackbar("HighS", "Control", &iHighS, 255);

   //createTrackbar("LowV", "Control", &iLowV, 255); //Value (0 - 255)
   //createTrackbar("HighV", "Control", &iHighV, 255);

  // For control of Circle Threshold
  //createTrackbar( "Threshold", "Control", &thresh, 255);
  //createTrackbar( "Max-Threshold", "Control", &max_thresh, 255);
  
  
   

   // Capture a temporary image from the camera
   Mat imgTmp;
   cap.read(imgTmp); 

   // Create a black image with the size as the camera output
   Mat imgLines = Mat::zeros( imgTmp.size(), CV_8UC3 );

   // main loop
   while (true)
   {
      int iLastX = -9999; 
      int iLastY = -9999;
      
      // read a new frame from video
      Mat imgOriginal;
      bool bSuccess = cap.read(imgOriginal); 

      // if not success, break loop
      if (!bSuccess) 
      {
	 cout << "Cannot read a frame from video stream" << endl;
	 break;
      }

      //Declare some Mat objects
      Mat imgHSV;
      Mat imgThresholded;

      //Convert the captured frame from BGR to HSV
      cvtColor(imgOriginal, imgHSV, COLOR_BGR2HSV);

      //Threshold the image
      inRange( imgHSV, Scalar(iLowH, iLowS, iLowV), Scalar(iHighH, iHighS, iHighV), imgThresholded); 
      
      //morphological opening (removes small objects from the foreground)
      erode( imgThresholded, imgThresholded, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)) );
      dilate( imgThresholded, imgThresholded, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)) ); 

      //morphological closing (removes small holes from the foreground)
      dilate( imgThresholded, imgThresholded, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)) ); 
      erode( imgThresholded, imgThresholded, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)) );


      //#####################################//
      //                                     //
      //          Draw on Threshold          //
      //                                     //
      //#####################################//
      //vector<vector<Point> >  contours;
      //vector<Vec4i> hierarchy;
      
      // Detect edges using Threshold
      //threshold( imgThresholded, imgThresholded, thresh, 255, THRESH_BINARY );

      //HoughCircles(imgThresholded, contours, CV_HOUGH_GRADIENT, 2, 50, 200, 100, 25, 100);
      
      
      // Find contours
      //findContours( imgThresholded, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );
      
     
      // Approximate contours to polygons + get bounding rects and circles
      //vector<vector<Point> > contours_poly( contours.size() );
      //vector<Rect> boundRect( contours.size() );
      //vector<Point2f>center( contours.size() );
      //vector<float>radius( contours.size() );

      //for( unsigned int i = 0; i < contours.size(); i++ )
      //{
	   
	 //approxPolyDP( Mat(contours[i]), contours_poly[i], 3, true );
	 //boundRect[i] = boundingRect( Mat(contours_poly[i]) );
	 //minEnclosingCircle( (Mat)contours_poly[i], center[i], radius[i] );
	  
	 //}

      // Draw polygonal contour + bonding rects + circles
      // Mat drawing = Mat::zeros( imgThresholded.size(), CV_8UC3 );
      //for( unsigned int i = 0; i< contours.size(); i++ )
      //{
	 // currently random colors
      //Scalar color = Scalar( 255, 255, 0 );
	  
      // drawContours( imgThresholded, contours_poly, i, color, 1, 8, vector<Vec4i>(), 0, Point() );
	  
      // rectangle( imgThresholded, boundRect[i].tl(), boundRect[i].br(), color, 2, 8, 0 );
	  
      // circle( imgThresholded, center[i], (int)radius[i], color, 2, 8, 0 );
      //}
      
      //Calculate the moments of the thresholded image
      Moments oMoments = moments(imgThresholded);

      double dM01 = oMoments.m01;
      double dM10 = oMoments.m10;
      double dArea = oMoments.m00;
      
      // if the area <= 10000, I consider that the there are no object
      // in the image and it's because of the noise, the area is not zero 
      if (dArea > 10000)
      {
	 //calculate the position of the ball
	 int posX = dM10 / dArea;
	 int posY = dM01 / dArea;
	  
	 //if (iLastX >= 0 && iLastY >= 0 && posX >= 0 && posY >= 0)
	 //{
	    //Draw a red line from the previous point to the current point
	    //line(imgLines, Point(posX, posY), Point(iLastX, iLastY), Scalar(0,0,255), 2);
	 //}

	 //#############################
	 // x y positions are here
	 //#############################
	 iLastX = posX - 320;
	 iLastY = -(posY - 240);
      }

      // print to console
      cout << "X : " << iLastX << " Y : " << iLastY << "\n";
      
      imshow("Thresholded Image", imgThresholded);
      imshow("Original", imgOriginal);
      
      
      //wait for 'esc' key press for 30ms. If 'esc' key is pressed, break loop
      if (waitKey(30) == 27) 
      {
	 cout << "esc key is pressed by user" << endl;
	 break; 
      }
   }

   return 0;
}
