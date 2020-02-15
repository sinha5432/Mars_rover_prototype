#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from msg_pkg.msg import Driving_msg
from autonomous_task_pkg.msg import Decider


out=Driving_msg()

driving_linear=0
driving_angular=0

auto_linear=0
auto_angular=0

flag=0
def driving_callback(msg):
	global gps_status
	global driving_linear
	global driving_angular
	global flag
	global out
	
	driving_linear=msg.twist.linear.x
	driving_angular=msg.twist.angular.z
	out.m1=msg.m1
	out.m2=msg.m2
	out.reset=msg.reset

	if(flag==0):
		out.twist.linear.x=driving_linear
		out.twist.angular.z=driving_angular
		print('driving')
	else:
		out.twist.linear.x=auto_linear
		out.twist.angular.z=auto_angular
		print('autonomous')
	print(out)
	pub.publish(out)
	

def autonomous_callback(msg,pub):
	global gps_status
	global auto_linear
	global auto_angular
	global flag
	global out
	
	auto_linear=msg.linear.x
	auto_angular=msg.angular.z


	if(flag==0):
		out.twist.linear.x=driving_linear
		out.twist.angular.z=driving_angular
		print('driving')
	else:
		out.twist.linear.x=auto_linear
		out.twist.angular.z=auto_angular
		print('autonomous')
	print(out)
	pub.publish(out)

def joy_callback(msg):
	global flag
	if(msg.buttons[7]==1):
		if(flag==0):
			flag=1
		else:
			flag=0

if __name__ == '__main__':
	rospy.init_node('switch_node')
	pub = rospy.Publisher('/cmd_vel', Driving_msg, queue_size=1)	
	sub1 = rospy.Subscriber('/cmd_vel_manual', Driving_msg, driving_callback)
	sub2 = rospy.Subscriber('/cmd_vel_autonomous', Twist, autonomous_callback,pub)
	sub3 = rospy.Subscriber('/joy',Joy,joy_callback)
	rospy.spin()
