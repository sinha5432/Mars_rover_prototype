#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Pose
from math import atan2
from math import sqrt
from std_msgs.msg import Float64
from msg_pkg.msg import Decider_gps


x = 0.0
y = 0.0
x_linear=0
angle_to_goal = 0.0
p_error=0
z_angular=0
dis = 10

gps_flag=0


out=Decider_gps()
out.status=0



def callback(msg,pub):

	global angle_to_goal
	global p_error
	global z_angular
	global x_linear
	global gps_flag
	theta = msg.data
	theta = theta
	print("{}distance to goal".format(dis))
	error=angle_to_goal-theta

	if(error>180):
		error=error-360
	if(error<=-180):
		error=error+360
	
	#print("error_updated")
	print(error)
	kp=0.2
	kd=0
	if(dis<1):
		print("GOAL REACHED SUCCESSFULLY!!!!!!!")
		gps_flag=1
	if(gps_flag==0):
		if(error>10 or error<-10):
			z_angular=kp*error
			p_error=error
			print("setting angle::")
			if(z_angular>6):
				z_angular=6
				x_linear=0
			    
			elif(z_angular<-6):
				z_angular=-6
			 	x_linear=0

			elif(z_angular>0 and z_angular<3):
				z_angular=3
				x_linear=0

	    		elif(z_angular<0 and z_angular>-3):
				z_angular=-3
				x_linear=0
			
		else:
			print("Going Forward")

			if(dis>1):
		    		z_angular=0
		    		x_linear=7
			else:
				z_angular=0
		    		x_linear=0
	
    	
		if(z_angular!=0):
			out.twist.angular.z=z_angular
			out.twist.linear.x=0
			
		else:
			out.twist.angular.z=0
			out.twist.linear.x=x_linear

	
	if(gps_flag==1):
		out.twist.angular.z=0
		out.twist.linear.x=0

		pub.publish(out)

		print("GOAL REACHED SUCCESSFULLY!!!!!!!")
	if(dis<3):
		out.reach_flag=1
	else:
		out.reach_flag=0
	pub.publish(out)	


def newOdom(msg,pub):
	global x
	global y
	global dis
	global angle_to_goal
	global gps_flag
	global z_angular

	x = msg.position.x
	y =msg.position.y

	x=-x
	y=-y
	
	dis = ((x*x)+(y*y))
	dis=sqrt(dis)
	
	if(gps_flag==1):
		while(3>2):
			out.twist.angular.z=0
			out.twist.linear.x=0
			out.status=1
			print("GOAL REACHED SUCCESSFULLY!!!!!!!")
	if(dis<3):
		out.status=2
	if(dis<1):
		print("GOAL REACHED SUCCESSFULLY!!!!!!!")
		gps_flag=1
	

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

	if(dis<15):
		out.reach_flag=1
	else:
		out.reach_flag=0

	if(z_angular!=0):
		out.twist.angular.z=z_angular
		out.twist.linear.x=0
	else:
		out.twist.angular.z=0
		out.twist.linear.x=x_linear

	pub.publish(out)


if __name__ =='__main__' :
	rospy.init_node("speed_controller")
	pub = rospy.Publisher("/path_by_gps", Decider_gps, queue_size = 1)
	sub1 = rospy.Subscriber("/distance", Pose, newOdom,pub)
	sub2 = rospy.Subscriber("/imu_degree", Float64,callback,pub)
	rospy.spin()
