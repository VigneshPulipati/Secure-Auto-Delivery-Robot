#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist


def stop_robot(publisher):
    msg = Twist()

    for _ in range(10):
        publisher.publish(msg)
        rospy.sleep(0.05)


def main():

    rospy.init_node("robot_velocity_test")

    publisher = rospy.Publisher(
        "/cmd_vel",
        Twist,
        queue_size=10
    )

    rospy.loginfo("Robot velocity test started.")

    msg = Twist()
    msg.linear.x = 0.15
    msg.angular.z = 0.0

    rospy.loginfo("Sending forward velocity for 2 seconds.")

    start_time = rospy.Time.now()

    while not rospy.is_shutdown():

        elapsed = (rospy.Time.now() - start_time).to_sec()

        if elapsed >= 2.0:
            break

        publisher.publish(msg)
        rospy.sleep(0.1)

    stop_robot(publisher)

    rospy.loginfo("Velocity test completed.")


if __name__ == "__main__":
    main()
