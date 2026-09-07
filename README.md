# infield_robotics_workshop
[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/ATB-potsdam-automation/infield_robotics_workshop)

## About
This repository contains material for the Infield Robotics Workshop of the VDI-Land.Technik / EurAgEng pre-conference. You can run the exercises using a local ROS 2 Jazzy installation or inside the included VS Code devcontainer.

## Requirements

- Ubuntu 24.04 with ROS 2 Jazzy
- `colcon` (`python3-colcon-common-extensions`)
- Docker and the VS Code Dev Containers extension when using the included container

## Installation

### Devcontainer

The `.devcontainer` configuration uses the `ros:jazzy` image. Reopen this repository in the container from VS Code; its post-create step builds the workspace with `colcon` and adds both ROS and the workspace setup files to `.bashrc`. The python scripts will be installed with --symlink-install meaning that you only have to change the orginal scripts and not rebuild after every change to python code.

### New colcon workspace

If you have an existing ROS 2 Jazzy environment you can also run the courses locally inside it.

Source ROS 2 Jazzy:

```sh
source /opt/ros/jazzy/setup.bash
```

Clone the workshop:

```sh
git clone https://github.com/ATB-potsdam-automation/infield_robotics_workshop.git
cd ~/infield_robotics_workshop
```

Build and source the workspace:

```sh
colcon build --symlink-install
source install/setup.bash
```

## Running the exercises

In one terminal:
Source the workspace (you can skip this inside the devcontainer as it is done automatically):

```sh
source /opt/ros/jazzy/setup.bash
source ~/infield_robotics_ws/install/setup.bash
```

and start the looping playback and foxglove bridge:

```sh
ros2 launch infield_robotics_workshop workshop.launch.py
```

In a second terminal, source the same setup (local env only) and run one exercise:

```sh
source /opt/ros/jazzy/setup.bash
source ~/infield_robotics_ws/install/setup.bash
```


```sh
ros2 run infield_robotics_workshop task1.py
```

Replace `task1.py` with `task2.py`, `task3.py`, `task4.py`, or `task5.py` for the other exercises. The task nodes enable simulated time automatically so they follow the playback clock.

The exercises build up the workflow in this order:

1. `task1.py`: subscribe to RFID and GPS topics and combine RFID detections with the latest GPS position.
2. `task2.py`: compare latest-GPS pairing with timestamp-based approximate synchronization.
3. `task3.py`: write RFID, GPS, and humidity data to a CSV file.
4. `task4.py`: look up the UAV pose using TF.
5. `task5.py`: apply transforms to position data.
