#!/usr/bin/env python

import roslib
import numpy
import rospy
import sys
from std_msgs.msg import String,Int32,Int32MultiArray,MultiArrayLayout,MultiArrayDimension
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats
import cv2
import numpy as np
import time


imagetosend=[]
data_to_send=Int32MultiArray()

################################################################################################


def main(args):
   pub=rospy.Publisher('avoid_image',Int32MultiArray,queue_size=2)
   rospy.init_node('avoid_image')
   r = rospy.Rate(2)
   while not rospy.is_shutdown():
        cap = cv2.VideoCapture(0)
        cap.isOpened()

        while(True):
            # Capture frame-by-frame
            ret, frame = cap.read()
            if ret:
                # Our operations on the frame come here
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                imgCanny = cv2.Canny(frame, 150, 200)  #Detecta bordes

                imgResize = cv2.resize(imgCanny,(500, 500)) #Cambia el ancho y alto de la imagen

                list=imgResize.tolist()

                

                #print("\nHello\n")
                #print(len(list))
                for i in range(len(list)):
                    for j in range(len(list)):
                        if list[i][j]>0:
                            list[i][j]=100
                        imagetosend.append(list[i][j])
                #print(list)
                #print(imagetosend)
                data_to_send.data=imagetosend
                pub.publish(data_to_send)
                r.sleep()   
                # Display the resulting frame
                cv2.imshow('frame',imgResize)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    rospy.on_shutdown()
                    break
       
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()   
        





if __name__ == '__main__':
    import sys, getopt
    main(sys.argv)








