#include "ros/ros.h"
#include "std_msgs/String.h"
#include <time.h>

using namespace std;

string selector = "camera";
time_t obs2_time = 9223372036854775807, cur_time = 0;

ros::Publisher pub_master;

std_msgs::String master_topic_msg;

// topic from slave
void camera_callback(const std_msgs::String::Ptr &sub_msg)
{
    ROS_INFO("camera_callback : %s", sub_msg->data.c_str());

    if (selector == "camera")
    {
        pub_master.publish(sub_msg);
    }
}

void lidar_callback(const std_msgs::String::Ptr &sub_msg)
{
    ROS_INFO("lidar_callback : %s", sub_msg->data.c_str());

    if (sub_msg->data == "NO")
    {
        selector = "camera";
    }
    else
    {
        selector = "lidar";
        pub_master.publish(sub_msg);

        if (sub_msg->data == "obstacle2") {
            obs2_time = time(NULL);
        }
    }
}

void color_callback(const std_msgs::String::Ptr &sub_msg)
{
    cur_time = time(NULL);
    if(cur_time - obs2_time > 8) {
        ROS_INFO("color_callback : %s", sub_msg->data.c_str());

        if (sub_msg->data == "RED")
        {
            selector = "red";
            pub_master.publish(sub_msg);
        }
        else if (sub_msg->data == "GREEN")
        {
            selector = "green";
            pub_master.publish(sub_msg);
        }
        else
        {
            selector = "camera";
        }
    }
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "master");
    ros::NodeHandle nh;

    pub_master = nh.advertise<std_msgs::String>("/direction", 1);
    ros::Subscriber sub_lidar = nh.subscribe("/lidar_direction", 1, lidar_callback);
    ros::Subscriber sub_camera = nh.subscribe("/camera_direction", 1, camera_callback);
    ros::Subscriber sub_color = nh.subscribe("/color_direction", 1, color_callback);

    ros::Rate loop_rate(1000);

    while (ros::ok())
    {
        ros::spinOnce();
        loop_rate.sleep();
    }

    return 0;
}
