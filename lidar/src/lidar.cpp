#include "ros/ros.h"
#include "std_msgs/String.h"

using namespace std;

int code_run = 0;
string master_msg = "";

// topic from master
void master_callback(const std_msgs::StringConstPtr &sub_msg) {
    master_msg = sub_msg->data.c_str();
    
    if(master_msg == "lidar") {
        code_run = 1;
    } else {
        code_run = 0;
    }
}

int main(int argc, char **argv) {
    ros::init(argc, argv, "lidar");
    ros::NodeHandle nh;

    // Publish topic from slave(lidar)
    ros::Publisher pub_lidar = nh.advertise<std_msgs::String>("/slave_topic", 1);
    // Subscribe topic from master
    ros::Subscriber sub_master = nh.subscribe("/master_topic", 1, master_callback);
    ros::Rate loop_rate(100);

    std_msgs::String slave_topic_msg;
    std::stringstream ss;
    ss << "lidar";
    slave_topic_msg.data = ss.str();

    while(ros::ok()) {
        ROS_INFO("%d", code_run);
        if (code_run) {
            ROS_INFO("lidar is running");
            pub_lidar.publish(slave_topic_msg);
        }

        ros::spinOnce();

        loop_rate.sleep();
    }

    return 0;
}