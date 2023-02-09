#include "ros/ros.h"
#include "std_msgs/String.h"

using namespace std;

string selector = "camera";

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
    }
}

void color_callback(const std_msgs::String::Ptr &sub_msg)
{
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
