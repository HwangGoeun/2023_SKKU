#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import time
import enum
import numpy as np 
import random
import rospy
from std_msgs.msg import String

direction_pub = rospy.Publisher('direction', String, queue_size=1)

width = 640
height = 480


cap = cv2.VideoCapture(2)              
cap.set(3,width)           #크롭사이즈
cap.set(4,height)

#----------------------------
brightness=10
contrast=10
saturation=10
gain=10
DETECT_VALUE = 200   #상대밝기
#----------------------------

cap.set(cv2.CAP_PROP_BRIGHTNESS,brightness)    #카메라조도세팅
cap.set(cv2.CAP_PROP_CONTRAST,contrast)
cap.set(cv2.CAP_PROP_SATURATION,saturation)
cap.set(cv2.CAP_PROP_GAIN,gain)



min_x = 10               # 인식범위 사이즈
min_y = 200
  
direction = "GO"

while True : 
    
    direction_change = direction

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

    gray_frame = cv2.cvtColor(limited_frame, cv2.COLOR_RGB2GRAY)   
    
    dst_retval, dst_binaryzation = cv2.threshold(gray_frame, DETECT_VALUE, 255, cv2.THRESH_BINARY)  
    dst_binaryzation = cv2.erode(dst_binaryzation, None, iterations=1)   

    canny = cv2.Canny(dst_binaryzation, 255, 255)
    
    # cv2.imshow("canny", canny)
    
    leftLine = cv2.line(dst_binaryzation, (width/4, 0), (width/4, height), (0, 255, 0), 2, cv2.LINE_AA)
    midLine = cv2.line(dst_binaryzation, (2*width/4, 0), (2*width/4, height), (0, 255, 0), 2, cv2.LINE_AA)
    rightLine = cv2.line(dst_binaryzation, (3*width/4, 0), (3*width/4, height), (0, 255, 0), 2, cv2.LINE_AA)
    

    cv2.imshow("binaryzation",dst_binaryzation)              #차선인식
    

    histogram = list(np.sum(dst_binaryzation[:, :], axis=0)) 
    histogram_length = len(histogram)
   
    left = int(np.sum(histogram[:int(histogram_length/4)]))
    mid_left = int(np.sum(histogram[int(histogram_length/4):int(2*histogram_length/4)]))
    mid_right = int(np.sum(histogram[int(2*histogram_length/4):int(3*histogram_length/4)]))
    mid = int(np.sum(histogram[int(1*histogram_length/4):int(3*histogram_length/4)]))
    right = int(np.sum(histogram[int(3*histogram_length/4):]))



    
    rospy.init_node('direction_publisher')

    print("LEFT :", left, "MID-LEFT", mid_left, "MID :", mid, "MID-RIGHT", mid_right, "RIGHT : ", right)

#구간에 안들어가는 곳 체크하기
    # if right < 1000 :  ### 오른쪽에 차선이 안보이면 => 우회전
    #     direction = 4

    # else :           ### 오른쪽에 차선보임
    #     if mid_left < 1000 :   ### mid_left에 차선 안보임 => 직진
    #         direction = 1
        
    #     else :                 ### mid_left에 차선 보임 => 좌회전
    #         direction = 2

    # if left > 500000 :   ### left에 흰색 많이 보임 => 정지
    #     direction = 10
    if mid < 50000 : #x검검x
        if left < 50000 and right < 50000: #검검검검
            direction = "GO"
        else :
            if left < 50000 or right < 50000: 
                if left > right : #흰검검검
                    direction = "RIGHT"
                else : #검검검흰
                    direction = "LEFT"
            else : #흰검검흰
                direction = "GO"

    else :
        if mid_left > 50000 and mid_right > 50000: #x흰흰x
            if left > 50000 and right > 50000: #흰흰흰흰
                direction = "STOP"
            else :
                if left < 50000 and right < 50000: #검흰흰검
                    direction = "STOP"
                else :
                    if left > right : # 흰흰흰검
                        direction = "RIGHT"
                    else : #검흰흰흰
                        direction = "LEFT"
        else :
            if mid_left > 50000 : #x흰검x
                direction = "RIGHT"

            else : #x검흰x
                direction = "LEFT"




                

    cv2.putText(frame, direction, (width/2,height/2), cv2.FONT_ITALIC, 1, (0,0,255), 2)
    cv2.imshow("Ground Truth",frame)
    if direction_change != direction :
        if direction_change == "LEFT" and direction == "GO" :
            direction = "RIGHT"
        elif direction_change == "RIGHT" and direction == "GO" :
            direction = "LEFT"
        direction_pub.publish(direction)
    # elif direction == 10 :
    #     direction = 10
    # else :
    #     direction = 10

        


    k = cv2.waitKey(30) & 0xff   # ESC누르면 종료
    if k == 27: 
        break

print("------------[SHUT DOWN]------------")


cap.release()

exit()
