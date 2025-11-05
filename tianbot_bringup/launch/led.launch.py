import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration,TextSubstitution
from launch.actions import IncludeLaunchDescription,  DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    default_namespace = os.environ.get("TIANBOT_NAME", "")
    led_mode = os.environ.get("TIANBOT_LED_MODE", "cover")
    serial_port = os.environ.get("TIANBOT_LED_PORT", "/dev/tianbot_led")
    serial_baudrate = os.environ.get("TIANBOT_LED_BAUD", "115200")

    namespace = LaunchConfiguration('namespace')

    declare_namespace_cmd = DeclareLaunchArgument(
        "namespace", default_value=default_namespace, description="Top-level namespace"
    )

    ld = LaunchDescription()
    ld.add_action(declare_namespace_cmd)
    if "cover" in led_mode:
        ld.add_action(IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(
                get_package_share_directory("tianbot_led"),
                'launch', 'tianbot_led.launch.py'
            )),
            launch_arguments={'namespace': namespace,
                              'led_mode': led_mode,
                              'serial_port': serial_port,
                              'serial_baudrate': serial_baudrate,
                              }.items()
        ))
    # elif ...

    return ld