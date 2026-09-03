#!/bin/bash

# Autonomous Indoor Delivery Robot
# Emergency software stop

source /opt/ros/noetic/setup.bash

echo "Stopping robot motion..."

rostopic pub -1 /cmd_vel geometry_msgs/Twist \
'{
  linear:  {x: 0.0, y: 0.0, z: 0.0},
  angular: {x: 0.0, y: 0.0, z: 0.0}
}'

echo "Robot stop command sent."
