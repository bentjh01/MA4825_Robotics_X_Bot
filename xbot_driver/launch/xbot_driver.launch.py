import launch
import launch_ros.actions

def generate_launch_description():

    ld = launch.LaunchDescription()

    # Set the xbot_driver_path parameter
    ld.add_parameter(name='xbot_driver_path', value='$(find xbot_drivers)/src/driver.py')

    # Start the xbot_driver node with the specified parameters
    ld.add_action(launch_ros.actions.Node(
        package='xbot_driver',
        node_executable='xbot_driver_node',
        name='xbot_driver',
        parameters=[{
            '/robot_name': '/xbot',
            '/controller_name': '/xbot/simple_controller'
        }]
    ))

    return ld

if __name__ == '__main__':
    launch.launch(generate_launch_description())
