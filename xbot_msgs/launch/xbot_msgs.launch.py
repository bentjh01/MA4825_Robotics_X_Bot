import launch
import launch_ros.actions

def generate_launch_description():

    ld = launch.LaunchDescription()

    # Start a ROS node to publish sensor readings
    ld.add_action(launch_ros.actions.Node(
        package='my_package',
        node_executable='sensor_publisher_node'
    ))

    # Start a ROS node to subscribe to sensor readings and control the robot
    ld.add_action(launch_ros.actions.Node(
        package='my_package',
        node_executable='robot_controller_node'
    ))

    return ld

if __name__ == '__main__':
    launch.launch(generate_launch_description())
