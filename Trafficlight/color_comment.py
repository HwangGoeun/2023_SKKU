    #!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import time
import enum
import numpy as np 
import random
import rospy
from std_msgs.msg import String

def callback(msg):
    if msg == "STOP" :
        traffic_pub = rospy.Publisher('/color', String, queue_size=1)
        

        width = 1280  # 카메라 가로사이즈
        height = 720  # 카메라 세로사이즈
        min_x = 200        # 인식범위 사이즈
        min_y = 200

        cap = cv2.VideoCapture(3)         #카메라 포트번호           
        cap.set(3,width)           #크롭사이즈
        cap.set(4,height)

        #----------------------------
        brightness=10    #brightness_reset.py에서 값 얻기 보통 DETECT_VALUE만 수정
        contrast=10
        saturation=10
        gain=10
        DETECT_VALUE = 250   #상대밝기  대회장에서는 250
        #----------------------------

        cap.set(cv2.CAP_PROP_BRIGHTNESS,brightness)    #카메라조도세팅
        cap.set(cv2.CAP_PROP_CONTRAST,contrast)
        cap.set(cv2.CAP_PROP_SATURATION,saturation)
        cap.set(cv2.CAP_PROP_GAIN,gain)

        color = "NOT GREEN"

        while True : 

            ret, frame = cap.read()

            max_x = width - min_x
            max_y = height - min_y
            
                
            limited_polylines_list = [[min_x, max_y],  [max_x,max_y], [max_x, min_y], [min_x, min_y]]
            limited_polylines_list_1 = [[min_x-2, max_y+2],  [max_x+2, max_y+2], [max_x+2, min_y-2], [min_x-2, min_y-2]]

            pts = np.array(limited_polylines_list_1, np.int32)
            pts = pts.reshape((-1,1,2))
            cv2.polylines(frame, [pts],True, (255, 0, 0), 2)
            
            
            matSrc = np.float32(limited_polylines_list)
            matDst = np.float32([[0,height], [width,height], [width,0], [0,0]])
            matAffine = cv2.getPerspectiveTransform(matSrc,matDst)
            limited_frame = cv2.warpPerspective(frame,matAffine,(width,height))

            limited_frame_copy = limited_frame.copy()
            hsv = cv2.cvtColor(limited_frame_copy, cv2.COLOR_BGR2HSV)
            hue,_,_ = cv2.split(hsv)
            mean_of_hue = cv2.mean(hue)[0]

            hue = cv2.inRange(hue,70, 90)  #초록색은 70-~90
            
            mean_of_hue = cv2.mean(hue)[0]   #ROI 휴값 평균
            cv2.imshow("ground truth",frame)
            cv2.imshow("color detection",limited_frame_copy)
            print(mean_of_hue)
            if mean_of_hue > 80:     # 초록색만 숫자큼
                color = "GREEN"
            else :
                color = "NOT GREEN"
        
            rospy.init_node('traffic_publisher')
            traffic_pub.publish(color)

            k = cv2.waitKey(30) & 0xff   # ESC누르면 종료
            if k == 27: 
                break
    else :
        rate.sleep()
    
rospy.init_node('direction_subscriber')
sub = rospy.Subscriber('/direction', String, callback)
rospy.spin()



print("------------[SHUT DOWN]------------")
cap.release()
exit()