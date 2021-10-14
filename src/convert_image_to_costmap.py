#!/usr/bin/env python

import roslib
import numpy
import rospy
import sys
from std_msgs.msg import *
from nav_msgs.msg import *
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats
import cv2
import numpy as np
import time

width=500
height=500


imagetosend=[0] * (width*height)

data_to_send=Int8MultiArray()
map_to_send=OccupancyGrid()

################################################################################################


def main(args):
   pub=rospy.Publisher('avoid_image',Int8MultiArray,queue_size=1)
   pub_map=rospy.Publisher('avoid_map',OccupancyGrid,queue_size=1)
   rospy.init_node('avoid_image')
   r = rospy.Rate(100)
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

                imgResize = cv2.resize(imgCanny,(width, height)) #Cambia el ancho y alto de la imagen

                list=imgResize.tolist()

                

                #print("\nHello\n")
                #print(len(list))

                k=0

                for i in range(len(list)):
                    for j in range(len(list)):
                        if list[i][j]>0:
                            list[i][j]=100
                        imagetosend[k]=list[i][j] 
                        k+=1
                #print(list)
                #print(imagetosend)
                

                data_to_send.data=imagetosend

                #Datos del mapa a mandar
                map_to_send.header.frame_id = "base_link"
                map_to_send.info.width = width
                map_to_send.info.height = height
                map_to_send.info.resolution = 0.01
                map_to_send.info.origin.position.x = 1
                map_to_send.info.origin.position.y = -0.5
                map_to_send.info.origin.position.z = 0
                map_to_send.info.origin.orientation.z = 1
                map_to_send.info.origin.orientation.w = 1



                map_to_send.data=imagetosend
                pub_map.publish(map_to_send)

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








