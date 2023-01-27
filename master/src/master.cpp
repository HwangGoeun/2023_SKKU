#include "ros/ros.h"
#include "std_msgs/String.h"

using namespace std;

string slave_msg = "";
string drive = "drive";
string obstacle = "obstacle";

std_msgs::String master_topic_msg;

// topic from slave
void slave_callback(const std_msgs::String::Ptr& sub_msg) {
    slave_msg = sub_msg->data.c_str();
    ROS_INFO("Master subscribe : %s", sub_msg->data.c_str());

    if(slave_msg == "obstacle") {
        master_topic_msg.data = obstacle;
    }
    if(slave_msg == "drive") {
        master_topic_msg.data = drive;
    }
}

int main(int argc, char **argv) {
    ros::init(argc, argv, "master");
    ros::NodeHandle nh;

    ros::Publisher pub_master = nh.advertise<std_msgs::String>("/master_topic", 1);
    ros::Subscriber sub_master = nh.subscribe("/slave_topic", 1, slave_callback);
    ros::Rate loop_rate(10);

    master_topic_msg.data = drive;

    while(ros::ok()) {
        ros::spinOnce();
        loop_rate.sleep();

        pub_master.publish(master_topic_msg);
    }

    return 0;
}
