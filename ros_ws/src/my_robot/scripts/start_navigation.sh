#!/bin/bash

# Autonomous Indoor Delivery Robot
# Start autonomous navigation

set -e

source /opt/ros/noetic/setup.bash

if [ -f "$HOME/catkin_ws/devel/setup.bash" ]; then
    source "$HOME/catkin_ws/devel/setup.bash"
fi

echo "======================================"
echo " Autonomous Indoor Delivery Robot"
echo " Starting Navigation Stack"
echo "======================================"

roslaunch my_robot navigation.launch
