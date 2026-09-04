# Secure Auto Delivery Robot
## Automomous Delivery Robot With Smart Security System

An autonomous indoor delivery robot built on **ROS Noetic**, using LiDAR-based SLAM for mapping, `move_base` for autonomous navigation, an **ESP32** for low-level motor control, and a **QR-code unlock system** for verifying deliveries.

The robot maps an indoor space, autonomously navigates to a delivery point, and releases its cargo compartment only after scanning a QR code that matches a pending delivery record.

---

## Features

- 🗺️ **SLAM mapping** — Hector SLAM + RPLiDAR for real-time indoor mapping
- 🧭 **Autonomous navigation** — `move_base` with tuned global/local costmaps and a waypoint-following client
- 🔌 **ESP32 motor bridge** — subscribes to `/cmd_vel` over `rosserial` and drives a differential-drive base through two L298N motor drivers
- 📦 **QR-based delivery unlock** — generates a unique QR code per delivery, verifies it against a local database, and actuates a servo to open/close the delivery box
- 🐳 **Dockerized ROS environment** — ARM64 image pre-loaded with all required ROS packages
- 🛠️ **Operator tooling** — shell scripts for diagnostics, map saving, navigation start/stop, and emergency stop

## Architecture

![System architecture diagram](/docs/adr_architecture.png)

The Raspberry Pi 5 (Ubuntu 24, Docker/ROS Noetic) acts as the central hardware and data bus, tying together three subsystems:

- **LIDAR and Navigation** — RPLiDAR publishes `/scan`, which feeds Hector SLAM to build `/map`; `move_base` consumes the map to plan and drive toward 2D nav goals.
- **Vision and Authentication** — the camera feed goes through QR detection, and a matched code triggers authentication (unlocking the delivery box).
- **Drive Control** — the ESP32 subscribes to `/cmd_vel` and drives two L298N motor drivers, each controlling three motors on the left/right side.

## Demo Videos

[SLAM](https://github.com/user-attachments/assets/a9ea2a0b-2393-4cc5-b9aa-b154f1bdec41) |
[Navigation](https://github.com/user-attachments/assets/c077286b-4bb8-4e33-ade5-128d4cb58a78)

## Repository Structure

```
.
├── docker/                    # Containerized ROS environment
│   ├── Dockerfile
│   └── run_container.sh
│
├── esp32/
│   └── motor_controller/
│       └── motor_controller.ino   # ESP32 firmware: /cmd_vel -> L298N motor drivers
│
├── ros_ws/src/my_robot/
│   ├── config/                 # Costmap & local planner parameters
│   ├── launch/                 # robot_bringup, slam, navigation, auto_nav, waypoint_navigation
│   ├── scripts/                # send_goal, waypoint_navigation, teleop_test, diagnostics
│   ├── CMakeLists.txt
│   └── package.xml
│
└── security/
    ├── qr_generation/           # Create a delivery record + QR code
    ├── qr_authentication/       # Scan QR, validate against DB, trigger unlock
    ├── qr_scanner/              # Standalone/reusable QR scanning module
    └── servo_controll/          # Servo-based box lock actuator
```

## Hardware

| Component | Role |
|---|---|
| Host computer (e.g. Raspberry Pi 4/5) | Runs ROS master, SLAM, navigation, QR/camera pipeline |
| RPLiDAR | 2D LiDAR for SLAM and obstacle avoidance |
| ESP32 | Runs `rosserial` firmware, drives motors from `/cmd_vel` |
| 2× L298N | Motor drivers — one per side (differential drive) |
| USB camera | QR code scanning for delivery verification |
| Servo motor | Locks/unlocks the delivery compartment |

**Default serial ports** (set in `robot_bringup.launch`):
- RPLiDAR → `/dev/ttyUSB0` @ 115200 baud
- ESP32 → `/dev/ttyUSB1` @ 57600 baud

## Getting Started

### 1. Build the Docker environment

```bash
cd docker
docker build -t secure-delivery-robot .
./run_container.sh
```

The image is based on `arm64v8/ros:noetic-ros-base` and includes `rplidar-ros`, `hector-slam`, `navigation`, `move_base`, `rosserial`, `map-server`, and the Python/OpenCV/QR dependencies.

### 2. Build the catkin workspace

Inside the container:

```bash
cd ~/catkin_ws
catkin_make
source devel/setup.bash
```

### 3. Flash the ESP32

Open `esp32/motor_controller/motor_controller.ino` in the Arduino IDE (with `rosserial_arduino` library installed), set the correct board/port, and flash it to the ESP32. It subscribes to `/cmd_vel` (`geometry_msgs/Twist`) at 57600 baud and drives the left/right motor pairs via two L298N drivers.

### 4. Bring up the robot

```bash
roslaunch my_robot robot_bringup.launch
```

This starts the RPLiDAR node, the `base_link -> laser` static transform, Hector SLAM, and the `rosserial` bridge to the ESP32.

### 5. Map the space

```bash
./ros_ws/src/my_robot/scripts/start_slam.sh
# drive the robot around (e.g. teleop_test.py) to build the map
./ros_ws/src/my_robot/scripts/save_map.sh room_map
```

### 6. Run autonomous navigation

```bash
roslaunch my_robot auto_nav.launch
```

or run the full stack manually via `robot_bringup.launch` + `navigation.launch`, then send goals with `scripts/send_goal.py` or run a preset route with `waypoint_navigation.launch`.

### 7. Delivery / QR unlock workflow

```bash
# 1. Create a delivery record and QR code
python3 security/qr_generation/generate_delivery.py

# 2. Print/display the generated QR_<id>.png for the recipient

# 3. On the robot, run the scanner/unlock service
python3 security/qr_authentication/qr_unlock.py
```

When a scanned QR code matches a pending `delivery_id` in `delivery_database.json`, the servo opens the compartment, then closes it automatically, and the delivery is marked `delivered`.

## Operator Scripts

| Script | Purpose |
|---|---|
| `scripts/check_robot.sh` | Diagnostics — checks USB devices, ROS master, key nodes/topics, and TF frames |
| `scripts/start_slam.sh` | Launches Hector SLAM |
| `scripts/start_navigation.sh` | Launches the navigation stack |
| `scripts/save_map.sh [name]` | Saves the current SLAM map via `map_server` |
| `scripts/stop_robot.sh` | Publishes a zero `Twist` to `/cmd_vel` as an emergency stop |
| `scripts/teleop_test.py` | Manual teleoperation for testing |
| `scripts/send_goal.py` | Send a single navigation goal |
| `scripts/waypoint_navigation.py` | Drive a predefined sequence of waypoints via `move_base` |

## License

MIT License — see [LICENSE](LICENSE).
