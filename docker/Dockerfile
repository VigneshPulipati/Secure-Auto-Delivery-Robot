FROM arm64v8/ros:noetic-ros-base

ENV DEBIAN_FRONTEND=noninteractive

SHELL ["/bin/bash", "-c"]

# ROS packages required by the robot
RUN apt-get update && apt-get install -y \
    ros-noetic-rplidar-ros \
    ros-noetic-hector-slam \
    ros-noetic-navigation \
    ros-noetic-move-base \
    ros-noetic-rosserial \
    ros-noetic-rosserial-python \
    ros-noetic-map-server \
    ros-noetic-tf \
    ros-noetic-rviz \
    python3-pip \
    python3-opencv \
    && rm -rf /var/lib/apt/lists/*

# Python packages used by the security system
RUN pip3 install --no-cache-dir \
    opencv-python \
    qrcode \
    pyzbar

# ROS environment
RUN echo "source /opt/ros/noetic/setup.bash" >> /root/.bashrc

WORKDIR /root/catkin_ws

CMD ["/bin/bash"]
