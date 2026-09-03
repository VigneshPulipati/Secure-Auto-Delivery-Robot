#!/bin/bash

# Autonomous Indoor Delivery Robot
# Save generated SLAM map

set -e

source /opt/ros/noetic/setup.bash

if [ -f "$HOME/catkin_ws/devel/setup.bash" ]; then
    source "$HOME/catkin_ws/devel/setup.bash"
fi

MAP_DIR="$(cd "$(dirname "$0")/../maps" && pwd)"

mkdir -p "$MAP_DIR"

MAP_NAME="${1:-room_map}"

echo "======================================"
echo " Saving SLAM Map"
echo " Location: $MAP_DIR/$MAP_NAME"
echo "======================================"

rosrun map_server map_saver \
    -f "$MAP_DIR/$MAP_NAME"

echo "Map saved successfully."
