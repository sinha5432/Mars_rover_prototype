#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32,Float64
from msg_pkg.msg import ultrasound_data,Arrow_feedback,Decider

out = Decider()
out.status=0
dist1=dist2=dist3=dist4=dist5=0
imu_angle = 0
n=0
arrow_flag=0
obstacle_flag=0
def left(): 
	out.twist.linear.x=0
	out.twist.angular.z=5
	#print("left")

def right():
	out.twist.linear.x=0
	out.twist.angular.z=-5
	#print("right")

def forward():
	out.twist.linear.x=6
	out.twist.angular.z=0
	#print("forward")

def backward():
	out.twist.linear.x=-6
	out.twist.angular.z=0
	#print("backward")

def stop():
	out.twist.linear.x=0.0
	out.twist.angular.z=0.0
	#print("stop")

def finding_obstacle():
	out.twist.linear.x=0.0
	out.twist.angular.z=3.0
	#print("obstacle finding")
	

def ultrasound_callback(msg,pub):
	global direction_flag,out
	global arrow_flag,n,obstacle_flag
	global dist1,dist2,dist3,dist4,dist5

	dist1=msg.dist1
	dist2=msg.dist2
	dist3=msg.dist3
	dist4=msg.dist4
	dist5=msg.dist5
	
	if(out.status==2 and obstacle_flag==0):
		out.status=2
		#print("Set By Arrow ")
	elif(out.status==2 and obstacle_flag==1):
		out.status=0
		print("Set By Arrow ")
	else :
		if(dist3<200 and dist3>80):
			forward()
			out.status=1
		elif(dist3<80 and dist3>30):
			stop()
			out.status=2
		elif((dist1<200 and dist1>30)or (dist2<200 and dist2>30) ):
			left()
			out.status=1
		elif(dist5<200 or dist4<200):
			right()
			out.status=1
		else:
			out.status=0
			finding_obstacle()
		#print("Set by Ultrasound")
	pub.publish(out)
	#print("-----------------------------------------")
	#print(out.status)

def arrow_callback(msg):
	global arrow_flag,obstacle_flag,n
	global direction_flag,out
	global dist1,dist2,dist3,dist4,dist5
	
	arrow_flag = msg.flag
	obstacle_flag = msg.obstacle_flag


	
	if(out.status==2 and obstacle_flag==0):
		out.status=2
		#print("Set By Arrow ")
	elif(out.status==2 and obstacle_flag==1):
		out.status=0
		print("Set By Arrow ")
	else :
		if(dist3<200 and dist3>80):
			forward()
			out.status=1
		elif(dist3<80 and dist3>30):
			stop()
			out.status=2
		elif((dist1<200 and dist1>30)or (dist2<200 and dist2>30) ):
			left()
			out.status=1
		elif(dist5<200 or dist4<200):
			right()
			out.status=1
		else:
			out.status=0
			finding_obstacle()
		#print("Set by Ultrasound")

if __name__ == '__main__':
	rospy.init_node('arrow_follower_node')
	pub = rospy.Publisher('/path_by_obstacle', Decider, queue_size=1)
	#pub = rospy.Publisher('/cmd_vel', Decider, queue_size=1)
	sub = rospy.Subscriber('/ultrasound_data',ultrasound_data,ultrasound_callback,pub)
	sub1 = rospy.Subscriber("/arrow", Arrow_feedback,arrow_callback)
	rospy.spin()
