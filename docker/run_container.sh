#!/bin/bash

# Autonomous Indoor Delivery Robot
# ROS Noetic Docker Environment

set -e

CONTAINER_NAME="delivery_robot_ros"

xhost +local:root 2>/dev/null || true

docker run -it \
    --privileged \
    --net=host \
    --device=/dev/rplidar:/dev/rplidar \
    --device=/dev/ttyUSB0:/dev/ttyUSB0 \
    --device=/dev/ttyUSB1:/dev/ttyUSB1 \
    --env="DISPLAY=${DISPLAY}" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --name="${CONTAINER_NAME}" \
    arm64v8/ros:noetic-ros-base \
    /bin/bash
