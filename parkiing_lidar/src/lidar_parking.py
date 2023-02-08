#! /usr/bin/env python3

import Function_Library as LiDAR
import rospy
from std_msgs.msg import String

# no_obstacle = True
# master_msg = ""
# lidar_msg = ""

pub_old = ""

def main():
    global pub_old
    rospy.init_node("RPLiDAR_sensing")

    # Publisher from lidar to master
    # pub_lidar = rospy.Publisher('/_topic', String, queue_size=1)
    
    # Publisher from lidar to arduino
    parking_pub = rospy.Publisher('/parking', String, queue_size=1)
    parking = "GO"

    env = LiDAR.libLIDAR('/dev/ttyUSB0')
    env.init()

    env.getState()

    count = 0

    for scan in env.scanning():
        count += 1

        left = env.getAngleDistanceRange(scan, 260, 350, 0, 1000)
        # left2 = env.getAngleDistanceRange(scan, 0, 10, 600, 1000)

        # go = env.getAngleDistanceRange(scan, 10, 60, 0, 400)
        # right = env.getAngleDistanceRange(scan, 11, 150, 0, 550)
        # go2 = env.getAngleDistanceRange(scan, 61, 120, 0, 400)

        if len(left):
            # print("obstacle")
            parking = "PARKING"
        else:
            parking = "GO"    # have to change "NO"
            # if len(right):
            #     print("right")
            #     direction = "right"
            # else:
            #     direction = "GO"
            #     print("GO")
                # if len(right):
                #     print("right")
                #     direction = "RIGHT"
                # else:


        # if count == 500:
        #     env.stop()
        #     break

        # 
        # 

        # if len(left):
        #     direction = "LEFT"
        # else:
        #     if len(go):
        #         direction = "GO"
        #     else:
        #         if len(right):
        #             direction = "RIGHT"
        # if pub_old != direction:
        parking_pub.publish(parking)

        # pub_old = direction        

    # while no_obstacle : 
    #     for scan in env.scanning():
    #         scan = env.getAngleDistanceRange(scan, 0, 30, 0, 300)
    #         count += 1

    #         # Find obstacles in range
    #         if len(scan):
    #             lidar_msg = "obstacle"
    #             pub_lidar.publish(lidar_msg)
    #             # env.stop()
    #             # no_obstacle = False
    #             # break

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
