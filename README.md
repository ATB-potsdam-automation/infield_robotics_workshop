# infield_robotics_workshop
[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/ATB-potsdam-automation/infield_robotics_workshop)

## About
This repository contains material for the Infield Robotics Workshop of the VDI-Land.Technik / EurAgEng pre-conference. You can run the exercises using a local ROS 2 Jazzy installation or inside the included VS Code devcontainer.

## Requirements

- Ubuntu 24.04 with ROS 2 Jazzy
- `colcon` (`python3-colcon-common-extensions`)
- Docker and the VS Code Dev Containers extension when using the included container

## Installation

### New colcon workspace

Source ROS 2 Jazzy:

```sh
source /opt/ros/jazzy/setup.bash
```

Create a workspace and clone the workshop into its `src` directory:

```sh
mkdir -p ~/infield_robotics_ws/src
cd ~/infield_robotics_ws/src
git clone https://github.com/ATB-potsdam-automation/infield_robotics_workshop.git
cd ~/infield_robotics_ws
```

Build and source the workspace:

```sh
colcon build --symlink-install
source install/setup.bash
```

### Existing colcon workspace

1. Source `/opt/ros/jazzy/setup.bash`.
2. Clone this repository into the workspace `src` directory.
3. From the workspace root, run `colcon build --symlink-install`.
4. Source `install/setup.bash` in every terminal that uses the package.

### Devcontainer

The `.devcontainer` configuration uses the `ros:jazzy` image. Reopen this repository in the container from VS Code; its post-create step builds the workspace with `colcon` and adds both ROS and the workspace setup files to `.bashrc`.

## Running the exercises

In one terminal, source the workspace and start the looping playback:

```sh
source /opt/ros/jazzy/setup.bash
source ~/infield_robotics_ws/install/setup.bash
ros2 launch infield_robotics_workshop workshop.launch.py
```

In a second terminal, source the same setup and run one exercise:

```sh
source /opt/ros/jazzy/setup.bash
source ~/infield_robotics_ws/install/setup.bash
ros2 run infield_robotics_workshop task1.py
```

Replace `task1.py` with `task2.py`, `task3.py`, `task4.py`, or `task5.py` for the other exercises. The task nodes enable simulated time automatically so they follow the playback clock.

The exercises build up the workflow in this order:

1. `task1.py`: subscribe to RFID and GPS topics and combine RFID detections with the latest GPS position.
2. `task2.py`: compare latest-GPS pairing with timestamp-based approximate synchronization.
3. `task3.py`: write RFID, GPS, and humidity data to a CSV file.
4. `task4.py`: look up the UAV pose using TF.
5. `task5.py`: apply transforms to position data.
