#!/usr/bin/env python
import rospy

from sensor_msgs.msg import Range
from msg_pkg.msg import ultrasound_data



rospy.init_node('ultrasound_data_combine')
out=ultrasound_data()

def callback1(msg,pub):
	if(msg.range<20 and msg.range>0):
		msg.range=500

	if(msg.range<0):
		msg.range=500

	if(msg.range != 0):
		out.dist1=msg.range
		pub.publish(out)
	print("published 1")
def callback2(msg,pub):
	
	if(msg.range<0):
		msg.range=500

	if(msg.range != 0):
		out.dist2=msg.range
		pub.publish(out)
	print("published 2")
def callback3(msg,pub):
	if(msg.range<20 and msg.range>0):
		msg.range=500

	if(msg.range<0):
		msg.range=500
	if(msg.range != 0):
		out.dist3=msg.range
		pub.publish(out)
	print("published 3")
def callback4(msg,pub):

	if(msg.range<0):
		msg.range=500
	if(msg.range != 0):
		out.dist4=msg.range
		pub.publish(out)
	print("published 4")
def callback5(msg,pub):
	#print("in callback 3")
	if(msg.range<0):
		msg.range=500
	if(msg.range !=0 ):
		out.dist5=msg.range
		pub.publish(out)
	print("published 5")


pub=rospy.Publisher('ultrasound_data',ultrasound_data,queue_size=50)
sub1=rospy.Subscriber('ultrasound1',Range,callback1,pub)
sub2=rospy.Subscriber('ultrasound2',Range,callback2,pub)
sub3=rospy.Subscriber('ultrasound3',Range,callback3,pub)
sub4=rospy.Subscriber('ultrasound4',Range,callback4,pub)
sub5=rospy.Subscriber('ultrasound5',Range,callback5,pub)
rospy.spin()
