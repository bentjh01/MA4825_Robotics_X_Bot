import launch
import launch_ros.actions

def generate_launch_description():

    ld = launch.LaunchDescription()

    # Add launch actions for all of the necessary ROS nodes and services here

    return ld

if __name__ == '__main__':
    launch.launch(generate_launch_description())