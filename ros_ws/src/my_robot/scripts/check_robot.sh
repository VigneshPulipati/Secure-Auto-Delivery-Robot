#!/bin/bash

# ============================================================
# Autonomous Indoor Delivery Robot
# Robot Diagnostic Utility
# ============================================================

source /opt/ros/noetic/setup.bash

if [ -f "$HOME/catkin_ws/devel/setup.bash" ]; then
    source "$HOME/catkin_ws/devel/setup.bash"
fi

echo ""
echo "=============================================="
echo "     AUTONOMOUS DELIVERY ROBOT DIAGNOSTICS"
echo "=============================================="

# ------------------------------------------------------------
# USB Devices
# ------------------------------------------------------------

echo ""
echo "[ USB DEVICES ]"

if [ -e /dev/ttyUSB0 ]; then
    echo "RPLIDAR : /dev/ttyUSB0  [FOUND]"
else
    echo "RPLIDAR : /dev/ttyUSB0  [NOT FOUND]"
fi

if [ -e /dev/ttyUSB1 ]; then
    echo "ESP32   : /dev/ttyUSB1  [FOUND]"
else
    echo "ESP32   : /dev/ttyUSB1  [NOT FOUND]"
fi


# ------------------------------------------------------------
# ROS Master
# ------------------------------------------------------------

echo ""
echo "[ ROS MASTER ]"

if rostopic list >/dev/null 2>&1; then
    echo "ROS Master : ONLINE"
else
    echo "ROS Master : OFFLINE"
    exit 1
fi


# ------------------------------------------------------------
# ROS Nodes
# ------------------------------------------------------------

echo ""
echo "[ ROS NODES ]"

check_node()
{
    if rosnode list 2>/dev/null | grep -qx "$1"; then
        echo "$1 : RUNNING"
    else
        echo "$1 : NOT RUNNING"
    fi
}

check_node "/rplidarNode"
check_node "/hector_mapping"
check_node "/move_base"
check_node "/esp32_bridge"


# ------------------------------------------------------------
# ROS Topics
# ------------------------------------------------------------

echo ""
echo "[ ROS TOPICS ]"

check_topic()
{
    if rostopic list 2>/dev/null | grep -qx "$1"; then
        echo "$1 : AVAILABLE"
    else
        echo "$1 : NOT AVAILABLE"
    fi
}

check_topic "/scan"
check_topic "/map"
check_topic "/cmd_vel"


# ------------------------------------------------------------
# TF
# ------------------------------------------------------------

echo ""
echo "[ TF FRAMES ]"

if rosrun tf tf_echo map base_link 2>/dev/null </dev/null >/dev/null; then
    echo "map -> base_link : AVAILABLE"
else
    echo "map -> base_link : NOT AVAILABLE"
fi

if rosrun tf tf_echo base_link laser 2>/dev/null </dev/null >/dev/null; then
    echo "base_link -> laser : AVAILABLE"
else
    echo "base_link -> laser : NOT AVAILABLE"
fi


# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

echo ""
echo "=============================================="
echo "              DIAGNOSTICS COMPLETE"
echo "=============================================="
echo ""
