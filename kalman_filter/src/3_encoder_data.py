#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64
from encoder_pkg.msg import Encoder_msg

out=Encoder_msg()

cpr=570
radius=0.0133

distance0=0
distance1=0
distance2=0
distance3=0

def callback_encoder0(msg,pub):
	global cpr
	global radius
	global distance0
	global distance1
	global distance2
	global distance3
	
	data=msg.data
	theta=data/cpr
	distance0=theta*2*3.14159*radius

	out.encoder0=distance0
	pub.publish(out)

def callback_encoder1(msg,pub):
	global cpr
	global radius
	global distance0
	global distance1
	global distance2
	global distance3
	
	data=msg.data
	theta=data/cpr
	distance1=theta*2*3.14159*radius
	

	out.encoder1=distance1
	pub.publish(out)

def callback_encoder2(msg,pub):
	global cpr
	global radius
	global distance0
	global distance1
	global distance2
	global distance3
	
	data=msg.data
	theta=data/cpr
	distance2=theta*2*3.14159*radius

	out.encoder2=distance2
	pub.publish(out)

def callback_encoder3(msg,pub):
	global cpr
	global radius
	global distance0
	global distance1
	global distance2
	global distance3
	
	data=msg.data
	theta=data/cpr
	distance3=theta*2*3.14159*radius

	out.encoder3=distance3
	pub.publish(out)




if __name__ == '__main__':
	rospy.init_node('encoders')
	pub = rospy.Publisher('/encoder',Encoder_msg, queue_size=100)
	sub1 = rospy.Subscriber('/encoder0_data',Float64,callback_encoder0,pub)
	sub2 = rospy.Subscriber('/encoder1_data',Float64,callback_encoder1,pub)
	sub3 = rospy.Subscriber('/encoder2_data',Float64,callback_encoder2,pub)
	sub4 = rospy.Subscriber('/encoder3_data',Float64,callback_encoder3,pub)
	rospy.spin()

