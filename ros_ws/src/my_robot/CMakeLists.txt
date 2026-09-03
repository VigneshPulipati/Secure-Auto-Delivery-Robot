cmake_minimum_required(VERSION 3.0.2)

project(my_robot)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  tf
  sensor_msgs
  geometry_msgs
  nav_msgs
  actionlib
  move_base_msgs
)

catkin_package()

include_directories(
  ${catkin_INCLUDE_DIRS}
)

catkin_install_python(
  PROGRAMS
    scripts/send_goal.py
    scripts/waypoint_navigation.py
  DESTINATION
    ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(
  DIRECTORY
    launch
    config
    scripts
    maps
    rviz
  DESTINATION
    ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
catkin_install_python(
  PROGRAMS
    scripts/send_goal.py
    scripts/waypoint_navigation.py
    scripts/teleop_test.py
  DESTINATION
    ${CATKIN_PACKAGE_BIN_DESTINATION}
)
catkin_install_python(
  PROGRAMS
    scripts/send_goal.py
    scripts/waypoint_navigation.py
    scripts/teleop_test.py
    scripts/navigation_status.py
  DESTINATION
    ${CATKIN_PACKAGE_BIN_DESTINATION}
)
