#!/usr/bin/env python


## this file takes data from encoder and converts it into accleration and velocity

import rospy
import numpy as np
import time
from kalman_filter.msg import vel_acc_msgs
from kalman_filter.msg import distance_msg
#from kalman_pkg.msg import Imu_data   ### import from manasvi
import math

flag = 0  ##defined for first time

dt = 0.01  ##initially dt = frequency of publisher encoder_distance
t1 = 0
vx = 0
vy = 0
ax = 0
ay = 0
px = 0
py = 0

pxn = 0
pyn = 0
vx_n = 0
vy_n = 0

theta = 0 ### check message type

def callback(msg,pub):
	out = vel_acc_msgs()
	global dt,px,py,vx,vy,ax,ay,theta,t1,flag
	if(flag!=0):
		dt = time.time() - t1
	t1 = time.time()
	distance = msg.d
	pxn = px + distance*(math.sin(theta))
	pyn = py + distance*(math.cos(theta))
	vxn = (pxn - px)/dt
	vyn = (pyn - py)/dt
	ax = (vxn - vx)/dt
	ay = (vyn - vy)/dt
	px = pxn
	py = pyn
	vx = vxn
	vy = vyn
	out.px_e = px
	out.py_e = py
	out.ax_e = ax
	out.ay_e = ay
	out.theta = theta
	print(out)
	print(dt)
	flag = 1 ## completion of first loop
	pub.publish(out)



rospy.init_node('vel_acc_values')
pub = rospy.Publisher('/vel_acc_pos',vel_acc_msgs,queue_size = 1)
sub = rospy.Subscriber('/encoder_distance',distance_msg,callback,pub)
#sub = rospy.Subscriber('/imu_data_filtered',Imu_data,imu_callback)
rospy.spin()
