import rospy
from std_msgs.msg import Bool
import Jetson.GPIO as GPIO

def main():
   channel = 15
   GPIO.setmode(GPIO.BOARD)
   GPIO.setup(channels = channel, direction = GPIO.IN)
   topic_name = "/limit_switch"
   limitSwitchPublusher = rospy.Publisher(topic_name, Bool, queue_size=10)
   rospy.init_node('LimitSwitchWatcher')
   rate = rospy.Rate(10)
   while not rospy.is_shutdown():
      status = GPIO.input(channel)
      msg = Bool()
      msg.data = bool(status)
      limitSwitchPublusher.publish(msg)
      rospy.loginfo(msg)
      rate.sleep()
   GPIO.cleanup()

if __name__ == '__main__':
   try:
      main()
   except rospy.ROSInterruptException:
      pass