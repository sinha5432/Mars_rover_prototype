#!/usr/bin/env python
import rospy

from geometry_msgs.msg import Twist
#from sensor_msgs.msg import Range
from autonomous_task_pkg.msg import ultrasound_data
from msg_pkg.msg import Decider
import time


rospy.init_node('obstacle_avoider')
out=Decider()



def left():  
	out.twist.linear.x=0
	out.twist.angular.z=6
	print("left")
	out.status=1

def right():
	out.twist.linear.x=0
	out.twist.angular.z=-6
	print("right")
	out.status=1

def forward():
	out.twist.linear.x=7
	out.twist.angular.z=0
	print("forward")
	out.status=0

def forward_slow():
	out.twist.linear.x=4
	out.twist.angular.z=0
	print("forward slow")
	out.status=1

def backward():
	out.twist.linear.x=-6
	out.twist.angular.z=0
	print("backward")
	out.status=1

def stop():
	out.twist.linear.x=0
	out.twist.angular.z=0
	print("stop")
	out.status=0

r=rospy.Rate(200)

def callback(msg,pub):


	dist1=msg.dist1
	dist2=msg.dist2
	dist3=msg.dist3
	dist4=msg.dist4
	dist5=msg.dist5



	if(dist1==500 and dist2==500 and dist3==500 and dist5==500 and dist5==500):
		forward()
		
	elif(dist1<100 or dist2<100 or dist3<100 or dist4<100 or dist5<100):
		backward()
	
	elif(dist1<150 and dist2<0 and dist3<0 and dist4<0 and dist5<0):
		right()

	elif(dist1<0 and dist2<150 and dist3<0 and dist4<0 and dist5<0):
		right()
		
	
	elif(dist1<0 and dist2<0 and dist3<150 and dist4<0 and dist5<0):
		right()

	elif(dist1<0 and dist2<0 and dist3<0 and dist4<150 and dist5<0):
		left()

	elif(dist1<0 and dist2<0 and dist3<0 and dist4<0 and dist5<150):
		left()

	elif(dist1<0 and dist2<150 and dist3<0 and dist4<150 and dist5<0):
		forward_slow()

	elif(dist1<150):
		right()

	elif(dist2<150):
		right()
		
	elif(dist3<150):
		left()
		
	elif(dist4<150):
		left()
		

	elif(dist5<150):
		left()
		
	else:
		forward()

	pub.publish(out)

pub=rospy.Publisher('/path_by_obstacle',Decider,queue_size=1)
sub=rospy.Subscriber('ultrasound_data',ultrasound_data,callback,pub)

rospy.spin()
