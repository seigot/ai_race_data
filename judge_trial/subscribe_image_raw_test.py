#!/usr/bin/env python
import rospy
import time
from sensor_msgs.msg import Image
from std_msgs.msg import Float32
from std_msgs.msg import Float64

now = time.time()
pre = time.time()

def set_throttle_steer(data):
    global pre
    global now
    now = time.time()
    print ("subscribe image time:{0}".format((now - pre)) + "[sec]")
    pre = now
    
def inference_from_image():
    rospy.init_node('inference_from_image', anonymous=True)
    rospy.Subscriber("/front_camera/image_raw", Image, set_throttle_steer)
    r = rospy.Rate(10)
    rospy.spin()

if __name__ == '__main__':
    try:
        inference_from_image()
    except rospy.ROSInterruptException:
        pass
