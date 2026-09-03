#!/bin/bash

# Autonomous Indoor Delivery Robot
# Start Hector SLAM

set -e

source /opt/ros/noetic/setup.bash

if [ -f "$HOME/catkin_ws/devel/setup.bash" ]; then
    source "$HOME/catkin_ws/devel/setup.bash"
fi

echo "======================================"
echo " Autonomous Indoor Delivery Robot"
echo " Starting Hector SLAM"
echo "======================================"

roslaunch my_robot slam.launch
