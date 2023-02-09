#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import rospy
from std_msgs.msg import String

direction_pub = rospy.Publisher('/camera_direction', String, queue_size=1)

width = 1280
height = 720
min_x = 5      # 인식범위 사이즈
min_y = 450
max_x = width - 50
max_y = height - 50

cap = cv2.VideoCapture(4)              
cap.set(3,width)           #크롭사이즈
cap.set(4,height)

#----------------------------
brightness=100
contrast=10
saturation=10
gain=10
DETECT_VALUE = 150   #상대밝기
#----------------------------

cap.set(cv2.CAP_PROP_BRIGHTNESS,brightness)    #카메라조도세팅
cap.set(cv2.CAP_PROP_CONTRAST,contrast)
cap.set(cv2.CAP_PROP_SATURATION,saturation)
cap.set(cv2.CAP_PROP_GAIN,gain)

direction = "GO"

while True : 
    
    direction_change = direction

    ret, frame = cap.read()


    
        
    limited_polylines_list = [[min_x, max_y],  [max_x,max_y], [max_x, min_y], [min_x+200, min_y]]
    limited_polylines_list_1 = [[min_x-2, max_y+2],  [max_x+2, max_y+2], [max_x+2, min_y-2], [min_x-2+200, min_y-2]]

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
    
    # leftLine = cv2.line(dst_binaryzation, (width/4, 0), (width/4, height), (0, 255, 0), 2, cv2.LINE_AA)
    # midLine = cv2.line(dst_binaryzation, (2*width/4, 0), (2*width/4, height), (0, 255, 0), 2, cv2.LINE_AA)
    # rightLine = cv2.line(dst_binaryzation, (3*width/4, 0), (3*width/4, height), (0, 255, 0), 2, cv2.LINE_AA)
    
    cv2.imshow("binaryzation",dst_binaryzation)              #차선인식

    histogram = list(np.sum(dst_binaryzation[:, :], axis=0)) 
    histogram_length = len(histogram)
   
    left = int(np.sum(histogram[:int(histogram_length/4)]))
    mid_left = int(np.sum(histogram[int(histogram_length/4):int(2*histogram_length/4)]))
    mid_right = int(np.sum(histogram[int(2*histogram_length/4):int(3*histogram_length/4)]))
    mid = int(np.sum(histogram[int(1*histogram_length/4):int(3*histogram_length/4)]))
    right = int(np.sum(histogram[int(3*histogram_length/4):]))
    full = int(np.sum(histogram[:]))
    
    rospy.init_node('direction_publisher')

    print("LEFT :", left, "MID-LEFT", mid_left, "FULL :", full, "MID-RIGHT", mid_right, "RIGHT : ", right)

    if mid < 10000 : #x검검x
        if left < 10000 and right < 10000: #검검검검
            direction = "RIGHT"
        else :
            if left < 10000 or right < 10000: 
                if left > right : #흰검검검
                    direction = "RIGHT"
                else : #검검검흰
                    direction = "LEFT"
            else : #흰검검흰
                direction = "GO"

    else :
        if full > 87000000 :
            direction = "GO"
        else:
            
            if mid_left > 4000000 and mid_right > 4000000: #x흰흰x
                if right < 10000 :
                    direction = "LEFT"
                if left > 4000000 and right > 4000000: #흰흰흰흰
                    if full > 10000000 :
                        if left > right :
                            direction = "RIGHT"
                        else :
                            direction = "LEFT"
                else :
                    if left < 4000000 and right < 4000000: #검흰흰검
                        direction = "GO"
                    else :
                        if left > right : # 흰흰흰검
                            direction = "LEFT"
                        else : #검흰흰흰
                            direction = "GO"
            else :
                if mid_left > 4000000 : #x흰검x
                    direction = "RIGHT"

                else : #x검흰x
                    direction = "LEFT"

    # cv2.putText(frame, direction, (width/2,height/4), cv2.FONT_ITALIC, 1, (0,0,255), 2)
    cv2.imshow("Ground Truth",frame)
    # direction_pub.publish(direction)
    if direction_change != direction :
        direction_pub.publish(direction)

    k = cv2.waitKey(30) & 0xff   # ESC누르면 종료
    if k == 27: 
        direction = "LEFT"
        direction_pub.publish(direction)
        direction = "RIGHT"
        direction_pub.publish(direction)
        
direction = "STOP"
direction_pub.publish(direction)

print("------------[SHUT DOWN]------------")
cap.release()
exit()
