from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch.substitutions import FindExecutable
from launch_ros.actions import Node


def generate_launch_description():
    package_share = Path(get_package_share_directory('infield_robotics_workshop'))
    bag_directory = package_share / 'data' / '2022-11-15-21-15-53_ros2'

    return LaunchDescription([
        ExecuteProcess(
            cmd=[
                FindExecutable(name='ros2'),
                'bag',
                'play',
                '--clock',
                '--loop',
                str(bag_directory),
            ],
            output='screen',
        ),
        Node(
            package='foxglove_bridge',
            executable='foxglove_bridge',
            name='foxglove_bridge',
            output='screen',
            parameters=[{'port': 8765}],
        ),
    ])