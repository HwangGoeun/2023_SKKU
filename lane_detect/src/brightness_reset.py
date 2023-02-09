#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import time
import enum
import numpy as np 
import random



cap = cv2.VideoCapture(2)
cap.set(3,640) # set Width
cap.set(4,360) # set Height


brightness=10
contrast=10
saturation=10
gain=10
DETECT_VALUE = 200    #### 밝기 70 /130

k = cv2.waitKey(30) & 0xff


while True : 

    ret, frame = cap.read()

    if k == 27: # press 'ESC' to quit 
        brightness=int(input("[brightness] now : " + str(brightness) + " / new : "))
        contrast=int(input("[constrast] now : " + str(contrast) + " / new : "))
        saturation=int(input("[saturation] now : " + str(saturation) + " / new : "))
        gain=int(input("[gain] now : " + str(gain) + " / new : "))
        DETECT_VALUE=int(input("[detect_value] now : " + str(DETECT_VALUE) + " / new : "))

    cap.set(cv2.CAP_PROP_BRIGHTNESS,brightness)
    cap.set(cv2.CAP_PROP_CONTRAST,contrast)
    cap.set(cv2.CAP_PROP_SATURATION,saturation)
    cap.set(cv2.CAP_PROP_GAIN,gain)


    min_x = 10               # 인식범위 사이즈
    max_x = 630

    min_y = 10
    max_y = 350

    ####### polylines ###########

    limited_polylines_list = [[min_x, max_y],  [max_x,max_y], [max_x, min_y], [min_x, min_y]]
    limited_polylines_list_1 = [[min_x-2, max_y+2],  [max_x+2, max_y+2], [max_x+2, min_y-2], [min_x-2, min_y-2]]
    pts = np.array(limited_polylines_list_1, np.int32)
    pts = pts.reshape((-1,1,2))
    cv2.polylines(frame, [pts],True, (0, 255, 0), 2) 
    cv2.imshow("1_polylines",frame)
    


    matSrc = np.float32(limited_polylines_list)
    matDst = np.float32([[0,360], [640,360], [640,0], [0,0]])
    matAffine = cv2.getPerspectiveTransform(matSrc,matDst)# mat 1 src 2 dst
    limited_frame = cv2.warpPerspective(frame,matAffine,(640,360))

    #cv2.imshow("2_limited_frame",limited_frame)




    #####  gray ############
    gray_frame = cv2.cvtColor(limited_frame, cv2.COLOR_RGB2GRAY)   
    # gray_frame = cv2.Canny(gray_frame,105,105)
    
    dst_retval, dst_binaryzation = cv2.threshold(gray_frame, DETECT_VALUE, 255, cv2.THRESH_BINARY)   #### 밝기부분
    dst_binaryzation = cv2.erode(dst_binaryzation, None, iterations=1)   



    #cv2.imshow("3_gray_frame",gray_frame)
    cv2.imshow("4_dst_binaryzation",dst_binaryzation)

    # histogram = list(np.sum(dst_binaryzation[dst_binaryzation.shape[0]//2:, :], axis=0)) 
    histogram = list(np.sum(dst_binaryzation[:, :], axis=0))   ##### 전체를 읽어서, 판단함.
    histogram_length = len(histogram)
   

    left = int(np.sum(histogram[:int(histogram_length/4)]))
    right = int(np.sum(histogram[int(3*histogram_length/4):]))
    
    up = np.sum(histogram[int(histogram_length/4):int(3*histogram_length/4)])
    
    left = int(np.sum(histogram[:int(histogram_length/4)]))
    mid_left = int(np.sum(histogram[int(histogram_length/4):int(2*histogram_length/4)]))
    mid_right = int(np.sum(histogram[int(2*histogram_length/4):int(3*histogram_length/4)]))
    mid = int(np.sum(histogram[int(1*histogram_length/4):int(3*histogram_length/4)]))
    right = int(np.sum(histogram[int(3*histogram_length/4):]))

    print("LEFT :", left, "MID-LEFT", mid_left, "MID :", mid, "MID-RIGHT", mid_right, "RIGHT : ", right)

    # if ( abs(right-left) > 500000) : 

    #     if right > left :  ### right 방향일 경우에... 
    #         direction = "RIGHT"
            
    #         print ("                   [[ RIGHT ]]:" ,right-left)
    #         #Spin_Left()
            
    #     else :  #### Left 방향일 경우에 
    #         direction = "LEFT"
    #         print ("[[ LEFT ]]:", left-right)
    #         #Spin_Right()

    # else :  #### Up(직진) 방향일 경우에.... 
    #     print ("      [[ UP ]]:", up)




    k = cv2.waitKey(30) & 0xff
    


car.Car_Stop()
cap.release()
cv2.destroyAllWindows()
exit()