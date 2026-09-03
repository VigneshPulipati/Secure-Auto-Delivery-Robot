#!/usr/bin/env python3

import rospy
import actionlib

from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler


# Example waypoint sequence.
# Replace these values with coordinates from the saved map.
WAYPOINTS = [
    (0.0, 0.0, 0.0),
    (1.0, 0.0, 0.0),
    (1.0, 1.0, 1.57),
    (0.0, 1.0, 3.14),
]


def create_goal(x, y, yaw):

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

    return goal


def main():

    rospy.init_node("waypoint_navigation")

    client = actionlib.SimpleActionClient(
        "move_base",
        MoveBaseAction
    )

    rospy.loginfo("Waiting for move_base...")

    if not client.wait_for_server(rospy.Duration(30.0)):

        rospy.logerr("move_base server not available.")
        return

    rospy.loginfo(
        "Starting waypoint navigation."
    )

    for index, waypoint in enumerate(WAYPOINTS):

        x, y, yaw = waypoint

        rospy.loginfo(
            "Waypoint %d: x=%.2f y=%.2f yaw=%.2f",
            index + 1,
            x,
            y,
            yaw
        )

        goal = create_goal(x, y, yaw)

        client.send_goal(goal)

        client.wait_for_result()

        state = client.get_state()

        if state != GoalStatus.SUCCEEDED:

            rospy.logwarn(
                "Failed to reach waypoint %d.",
                index + 1
            )

            client.cancel_all_goals()
            return

        rospy.loginfo(
            "Waypoint %d reached.",
            index + 1
        )

    rospy.loginfo(
        "All waypoints completed successfully."
    )


if __name__ == "__main__":
    main()
