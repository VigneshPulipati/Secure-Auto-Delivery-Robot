#!/usr/bin/env python3

import rospy

from move_base_msgs.msg import MoveBaseActionFeedback
from actionlib_msgs.msg import GoalStatus


STATUS_NAMES = {
    GoalStatus.PENDING: "PENDING",
    GoalStatus.ACTIVE: "ACTIVE",
    GoalStatus.PREEMPTED: "PREEMPTED",
    GoalStatus.SUCCEEDED: "SUCCEEDED",
    GoalStatus.ABORTED: "ABORTED",
    GoalStatus.REJECTED: "REJECTED",
    GoalStatus.PREEMPTING: "PREEMPTING",
    GoalStatus.RECALLING: "RECALLING",
    GoalStatus.RECALLED: "RECALLED",
    GoalStatus.LOST: "LOST",
}


def callback(msg):

    state = msg.status.status

    name = STATUS_NAMES.get(
        state,
        "UNKNOWN"
    )

    rospy.loginfo(
        "Navigation state: %s",
        name
    )


def main():

    rospy.init_node(
        "navigation_status"
    )

    rospy.Subscriber(
        "/move_base/feedback",
        MoveBaseActionFeedback,
        callback
    )

    rospy.loginfo(
        "Navigation status monitor started."
    )

    rospy.spin()


if __name__ == "__main__":
    main()
