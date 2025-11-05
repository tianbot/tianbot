# REF: https://github.com/danzimmerman/dz_launch_examples/blob/rolling/launch/opaque_multi_nodes.launch.py

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch.actions import OpaqueFunction

default_namespace = os.environ.get("TIANBOT_NAME", "/")
default_namespace = f"/" if default_namespace == ' ' or default_namespace =='/' else default_namespace
default_base = os.environ.get("TIANBOT_BASE", "tianbot_omni")
default_base_model = os.environ.get("TIANBOT_BASE_MODEL", "06q1")

def launch_setup(context, *args, **kwargs):
    namespace = LaunchConfiguration("namespace", \
        default=default_namespace).perform(context)
    base = LaunchConfiguration("base", \
        default=default_base).perform(context)
    base_model = LaunchConfiguration("base_model", \
        default=default_base_model).perform(context)
    return_node = []

    return_node.append(
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory("tianbot_description"),\
                    'launch', 'includes', f'{base}_{base_model}.launch.py')
            ),
            launch_arguments=[
                ('namespace', default_namespace)
            ]
    ))
    return return_node

def generate_launch_description():
    
    declared_args = []

    declared_args.append(
        DeclareLaunchArgument(
            "namesapce",
            default_value=default_namespace,
            description="robot name [tianbot_No1, tianbot_No2, tianbot_No3, ...]."
        )
    )

    declared_args.append(
        DeclareLaunchArgument(
            "base",
            default_value=default_base,
            description="mobile base type [tianbot, tianrover, tianbot_omni, tianbot_mini]."
        )
    )

    declared_args.append(
        DeclareLaunchArgument(
            "base_model",
            default_value=default_base_model,
            description="06q1, 06q2, 08q2, 08q8, 06s, rover, moon."
        )
    )

    return LaunchDescription(
        declared_args + [OpaqueFunction(function=launch_setup)],
    )