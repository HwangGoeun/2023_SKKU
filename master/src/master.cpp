#include "ros/ros.h"
#include "std_msgs/String.h"
#include <time.h>

using namespace std;

string selector = "camera"; //Initial selector = "camera" (selector is like a checkpoint)
time_t obs2_time = 9223372036854775807, cur_time = 0;

ros::Publisher pub_master;  //publisher name = pub_master

std_msgs::String master_topic_msg;

// topic from slave
void camera_callback(const std_msgs::String::Ptr &sub_msg)  //camera lane detection function
{
    ROS_INFO("camera_callback : %s", sub_msg->data.c_str());

    if (selector == "camera")
    {
        pub_master.publish(sub_msg);    //When selector is camera, publish sub_msg
    }
}

void lidar_callback(const std_msgs::String::Ptr &sub_msg)   //lidar obstacle function
{
    ROS_INFO("lidar_callback : %s", sub_msg->data.c_str());

    if (sub_msg->data == "NO")  //When lidar data is "NO", change selector = "camera". This means no obstacle detected.
    {
        selector = "camera";
    }
    else    //When obstacle is detected by lidar, change selector "lidar" and publish sub_msg. If lidar data is "obstacle2", obs2_time get current time.
    {
        selector = "lidar";
        pub_master.publish(sub_msg);

        if (sub_msg->data == "obstacle2") {
            obs2_time = time(NULL);
        }
    }
}

void color_callback(const std_msgs::String::Ptr &sub_msg)   //camera trafficlight detection function
{
    cur_time = time(NULL);
    if(cur_time - obs2_time > 8) {
        ROS_INFO("color_callback : %s", sub_msg->data.c_str()); //If 8s after detecting second obstacle, selector don't turn to "lidar".

        if (sub_msg->data == "RED") //If camera data is "RED", change selector "red", else if data is "GREEN", change selector "green"
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

    pub_master = nh.advertise<std_msgs::String>("/direction", 1);   //publish topic as /direction
    ros::Subscriber sub_lidar = nh.subscribe("/lidar_direction", 1, lidar_callback);    //subscribe topic as /lidar_direction
    ros::Subscriber sub_camera = nh.subscribe("/camera_direction", 1, camera_callback);    //subscribe topic as /camera_direction
    ros::Subscriber sub_color = nh.subscribe("/color_direction", 1, color_callback);    //subscribe topic as /color_direction

    ros::Rate loop_rate(1000);  //ros rate

    while (ros::ok())   //run ros
    {
        ros::spinOnce();
        loop_rate.sleep();
    }

    return 0;
}
