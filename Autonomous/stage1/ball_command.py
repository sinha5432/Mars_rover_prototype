#!/usr/bin/env python
import rospy

from geometry_msgs.msg import Twist
from msg_pkg.msg import ball_msg,Decider
import time


rospy.init_node('ball_follower')
out=Twist
p_error=0
count=0
flag_reached=0
stop_counter=0
out = Decider()

def stop():
	global out
	out.twist.linear.x=0
	out.twist.angular.z=0
	out.status = 1
	print("goal reached!!!!!")
	pub.publish(out)

def find_ball():
	global out
	out.twist.linear.x=0
	out.twist.angular.z=2.5
	out.status = 0
	print("Finding ball")
	pub.publish(out)
	


def callback(msg,pub):

	global p_error
	global out
	global count
	global flag_reached,stop_counter
	error=msg.x
	kd=0
	kp=0.005
	if(flag_reached==1):
		stop()
		stop_counter=0
		print("goal reached BY BALL detection!!!!!")
	elif(msg.detect==1):
		count=0
		t_error=kp*error
		if(error > 80):
			out.twist.linear.x = 0
			out.twist.angular.z = -3
			out.status = 1
			'''if out.twist.angular.z < 3:
				out.twist.angular.z = -3
			if out.twist.angular.z > 8:
				out.twist.angular.z = -8'''
			print("setting angle right")
			pub.publish(out)
		if(error < -80):
			out.twist.linear.x = 0
			out.twist.angular.z = 3
			'''if out.twist.angular.z < -3:
				out.twist.angular.z = 3
			if out.twist.angular.z > -8:
				out.twist.angular.z = 8'''
			print("setting angle left")
			pub.publish(out)
		if(error<80 and error>-80):
			if(msg.distance==1):
				out.twist.linear.x= 0
				out.twist.angular.z= 0
				out.status = 1
				print("goal reached!!!!!")
				pub.publish(out)
				flag_reached=1
			elif(msg.distance==1.5):
				out.twist.linear.x= 3 ## set forward
				out.twist.angular.z= 0
				out.status = 3
				flag_reached=0
				print("going forward(1.5):")
				pub.publish(out)

			else:
				out.twist.linear.x= 5 ## set forward
				out.twist.angular.z= 0
				flag_reached=0
				print("going forward:")
				pub.publish(out)

		if(out.twist.angular.z!=0):
			out.twist.linear.x=0
			out.status = 1
			pub.publish(out)
			#print("Setting angle:")'''
	else:
		if(count==10):
			#count=0
			if(stop_counter == 25000):
				stop()
			else:
				find_ball()
				'''time.sleep(0.5)
				pub.publish(out)
				stop()
				time.sleep(0.5)
				pub.publish(out)'''
				
				stop_counter = stop_counter+1	
				print(stop_counter)
		else:
			count = count+1
			


	#out.twist.linear.x=(out.twist.linear.x/25)
	#out.twist.angular.z=(out.twist.angular.z/25)

pub=rospy.Publisher('/path_by_ball',Decider,queue_size=1)
sub=rospy.Subscriber('/ball_publisher', ball_msg,callback,pub)

rospy.spin()
