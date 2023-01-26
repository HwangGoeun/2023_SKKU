#include "ros/ros.h"
#include "std_msgs/String.h"

// topic from slave
void slave_callback(const std_msgs::String::Ptr& sub_msg) {
    ROS_INFO("Master subscribe : %s", sub_msg->data.c_str());
}

int main(int argc, char **argv) {
    ros::init(argc, argv, "master");
    ros::NodeHandle nh;

    ros::Publisher pub_master = nh.advertise<std_msgs::String>("/master_topic", 1);
    ros::Subscriber sub_master = nh.subscribe("/slave_topic", 1, slave_callback);
    ros::Rate loop_rate(1000);

    std_msgs::String master_topic_msg;
    std::string drive = "drive";
    std::string lidar = "lidar";
    master_topic_msg.data = drive;

    int count = 0;

    while(ros::ok()) {
        if (count % 5 == 0) {
            master_topic_msg.data = lidar;
        } else {
            master_topic_msg.data = drive;
        }
        pub_master.publish(master_topic_msg);

        count += 1;

        ros::spinOnce();

        loop_rate.sleep();
    }

    return 0;
}
