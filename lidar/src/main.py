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
    direction_pub = rospy.Publisher('direction', String, queue_size=1)
    direction = "GO"

    # LiDAR sensing
    env = LiDAR.libLIDAR('/dev/ttyUSB0')
    env.init()
    
    env.getState()

    for scan in env.scanning():
        left = env.getAngleDistanceRange(scan, 0, 30, 0, 500)
        go = env.getAngleDistanceRange(scan, 31, 150, 0, 300)
        right = env.getAngleDistanceRange(scan, 151, 180, 0, 1000)

        if len(left):
            direction = "LEFT"
        else:
            if len(go):
                direction = "GO"
            else:
                if len(right):
                    direction = "RIGHT"
                else:
                    direction = ""

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
        if pub_old != direction:
            direction_pub.publish(direction)

        pub_old = direction        

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
        env.stop()
        pass