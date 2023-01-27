#! /usr/bin/env python3

import Function_Library as LiDAR
import rospy
from std_msgs.msg import String

no_obstacle = True
master_msg = ""
lidar_msg = ""

def main():
    rospy.init_node("RPLiDAR_sensing")

    # Publisher from lidar to master
    pub_lidar = rospy.Publisher('/slave_topic', String, queue_size=1)
    
    # LiDAR sensing
    env = LiDAR.libLIDAR('/dev/ttyUSB0')
    env.init()
    
    env.getState()

    while no_obstacle : 
        for scan in env.scanning():
            scan = env.getAngleDistanceRange(scan, 0, 30, 0, 300)
            count += 1

            # Find obstacles in range
            if len(scan):
                lidar_msg = "obstacle"
                pub_lidar.publish(lidar_msg)
                env.stop()
                no_obstacle = False
                break

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass