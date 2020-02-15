#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Pose
from std_msgs.msg import Int32,Float64
from math import atan2

x = 0
y = 0
angle_to_goal = 0
p_error=0
out = Int32()

def callback_compass(msg,pub):
	global angle_to_goal
	global p_error
	current = msg.data ##check
	error =  current-angle_to_goal
	kp=0.8
	kd=0.7

	if(error>180):
		error=error-360

	elif (error<=-180):
		error=error+360
	#print(error)
	z_angular=kp*error+kd*(error-p_error)

	if(error>3 or error<-3):
        	if(z_angular>0 and z_angular<120):
			z_angular=120		
    		elif(z_angular<0 and z_angular>-120):
			z_angular=-120
		if(z_angular>255):
			z_angular=255
		if(z_angular<-255):
			z_angular=-255
		'''if error>3:
			z_angular=250
		else:
			z_angular=-250'''
	else:
		z_angular=0

	out.data=z_angular
	
	#print("z_angular=")
	print(error)	
	p_error=error
	print(out)
	pub.publish(out)
	

def gps_callback(msg):
	global x
	global y
	global angle_to_goal
	x = msg.position.x
	y = msg.position.y
	
	if(x>0 and y>0):
		angle_to_goal=((atan2(y,x)*180)/3.141519)
		angle_to_goal=90-angle_to_goal
	elif(x>0 and y<0):
		angle_to_goal=((atan2((-1*y),x)*180)/3.141519)
		angle_to_goal=90+angle_to_goal
	elif(x<0 and y>0):
		angle_to_goal=((atan2(y,(-1*x))*180)/3.141519)
		angle_to_goal=270+angle_to_goal
	else:
		angle_to_goal=((atan2((-1*y),(-1*x))*180)/3.141519)
		angle_to_goal=270-angle_to_goal
	print("angle_to_goal=")
	print(angle_to_goal)

if __name__ == '__main__':
	rospy.init_node('antenna_dir_')
	pub = rospy.Publisher('/pwm', Int32, queue_size = 1)
	sub1 = rospy.Subscriber('/antenna_degree', Float64, callback_compass,pub) ##imu_callback
	sub2 = rospy.Subscriber('/distance', Pose, gps_callback) ##gps_callback
	rospy.spin()
	
