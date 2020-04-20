#!/usr/bin/env python

import rospy
from kalman_filter.msg import distance_msg
from kalman_filter.msg import Encoder_msg   ##message type for encoder values in distance

def callback(msg,pub):
	out = distance_msg()
	##weights decleration
	w1=1
	w0=1
	w2=1
	w3=1
	##assign encoders values 
	d0=msg.encoder0
	d1=msg.encoder1
	d2=msg.encoder2
	d3=msg.encoder3
	d = (w1*d1 + w2*d2 + w3*d3 + w0*d0)/(w1 + w2 + w3 + w0) ##calculation of average distance
	out.d = d
	print(d)
	pub.publish(out)
	rate.sleep()

rospy.init_node('encoder_distance_calculation')
pub = rospy.Publisher('encoder_distance',distance_msg,queue_size=1)
rate = rospy.Rate(10)
sub = rospy.Subscriber('/encoder',Encoder_msg,callback,pub)
rospy.spin()
