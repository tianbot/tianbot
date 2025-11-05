import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # mobile base type [tianbot, tianrover, tianbot_omni, tianbot_mini]
    base_type = os.environ.get("TIANBOT_BASE", "tianbot_omni")

    namespace = LaunchConfiguration(
        'namespace',
        default = '',
    )

    ld = LaunchDescription()
    ld.add_action(IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory("tianbot_bringup"),
            'launch', 'includes', f'{base_type}', 'mobile_base.launch.py'
        )),
        launch_arguments={'namesapce': namespace,
                            }.items()
    ))

    return ld