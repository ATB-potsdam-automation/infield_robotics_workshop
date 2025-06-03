#!/bin/bash
source /opt/ros/${ROS_DISTRO}/setup.bash
echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc
echo "source ~/infield_robotics_ws/devel/setup.bash" >> ~/.bashrc
catkin_make -C ~/infield_robotics_ws