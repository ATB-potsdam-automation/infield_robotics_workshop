#!/bin/bash
source /opt/ros/${ROS_DISTRO}/setup.bash
echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc
echo "source ~/infield_robotics_ws/install/setup.bash" >> ~/.bashrc
colcon build --symlink-install --base-paths ~/infield_robotics_ws/src