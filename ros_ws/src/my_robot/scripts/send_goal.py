#!/usr/bin/env python3

import sys

import rospy
import actionlib

from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler


def send_goal(x, y, yaw):

    rospy.init_node("navigation_goal_sender")

    client = actionlib.SimpleActionClient(
        "move_base",
        MoveBaseAction
    )

    rospy.loginfo("Waiting for move_base...")

    if not client.wait_for_server(rospy.Duration(30.0)):
        rospy.logerr("move_base server not available.")
        return False

    goal = MoveBaseGoal()

    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()

    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y

    quaternion = quaternion_from_euler(
        0.0,
        0.0,
        yaw
    )

    goal.target_pose.pose.orientation.x = quaternion[0]
    goal.target_pose.pose.orientation.y = quaternion[1]
    goal.target_pose.pose.orientation.z = quaternion[2]
    goal.target_pose.pose.orientation.w = quaternion[3]

    rospy.loginfo(
        "Sending navigation goal: x=%.2f y=%.2f yaw=%.2f",
        x,
        y,
        yaw
    )

    client.send_goal(goal)

    client.wait_for_result()

    state = client.get_state()

    if state == GoalStatus.SUCCEEDED:

        rospy.loginfo("Navigation goal reached.")
        return True

    rospy.logwarn(
        "Navigation failed or cancelled. State: %d",
        state
    )

    return False


if __name__ == "__main__":

    if len(sys.argv) != 4:

        print(
            "Usage: send_goal.py <x> <y> <yaw>"
        )

        sys.exit(1)

    try:

        x = float(sys.argv[1])
        y = float(sys.argv[2])
        yaw = float(sys.argv[3])

    except ValueError:

        print("Error: coordinates and yaw must be numbers.")
        sys.exit(1)

    success = send_goal(x, y, yaw)

    sys.exit(0 if success else 1)
