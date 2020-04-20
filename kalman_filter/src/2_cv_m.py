#!/usr/bin/env python

import rospy
import numpy as np
from sensor_msgs.msg import NavSatFix
from std_msgs.msg import Float64
from kalman_filter.msg import covarience_values
from geometry_msgs.msg import Pose

i = 10
A = []
B = []
C = []
D = []
vx = []
vy = []
ax = []
ay = []
svx = svy = xp = yp = px = py = vxp = vyp = 0

n = -1
out = covarience_values()
def callback(msg,pub):
	global i,n,out,A,B,vx,vy,xp,yp,px,py,vxp,vyp,svx,svy
	px = msg.position.x
	py = msg.position.y
	if(n<9):
		A.append(px)
		B.append(py)
		xp = px
		yp = py

		vx1 = (px - xp)
		vy1 = (py - yp)
		vx.append(vx1)
		vy.append(vy1)

		ax.append(vx1 - vxp)
		ay.append(vy1 - vyp)

		n = n +1
	print(n)
	if (n+1 == i):
		out.x= np.mean(A)
		out.y= np.mean(B)
		out.sx= np.std(A)
		out.sy= np.std(B)
		out.svx= np.std(vx)
		out.svy= np.std(vy)
		out.sacc = max(np.std(ax), np.std(ay))
		print(out)

		while 1 :
			pub.publish(out)
			print("Done")

rospy.init_node('covarience_matrix_calculation')
pub = rospy.Publisher('/covarience_matrix' , covarience_values , queue_size = 5)
sub = rospy.Subscriber('/distance' , Pose , callback , pub)
rospy.spin()
