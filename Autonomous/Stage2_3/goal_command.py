#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Pose
from math import atan2
from math import sqrt
from std_msgs.msg import Float64
from msg_pkg.msg import Decider,Arrow_feedback 

x = 0.0
y = 0.0
x_linear=0
angle_to_goal = 0.0
p_error=0
z_angular=0
dis = 0
theta=0
obstacle_flag=0
gps_flag=0

arrow_final_flag=0
angle_by_arrow=0
out=Decider()
out.status=0



def imu_callback(msg,pub):

	global angle_to_goal
	global p_error
	global z_angular
	global x_linear
	global theta	
	global gps_flag
	global arrow_final_flag,angle_by_arrow
	theta = msg.data
	print("{}distance to goal".format(dis))
	print("{}flag ".format(gps_flag))
	error=angle_to_goal-theta
	print("error")
	print(error)
	if(error>180):
		error=error-360
	if(error<-180):
		error=error+360
	
	#print("error_updated")
	#print(error)
	kp=0.2
	kd=0
	if (gps_flag == 0 ):
		if(dis<1):
			print("GOAL REACHED SUCCESSFULLY!!!!!!!")
			gps_flag=1

        if(error>10 or error<-10):
        	differential=error-p_error
        	z_angular=kp*error+kd*differential
        	p_error=error
        	#print(kp)
		print("setting angle::")
        	if(z_angular>6):
        		z_angular=4
			x_linear=0
        	    
        	if(z_angular<-6):
        		z_angular=-4
		 	x_linear=0

		if(z_angular>0 and z_angular<3):
			z_angular=3
			x_linear=0

    		if(z_angular<0 and z_angular>-3):
			z_angular=-3
			x_linear=0
        	
	else:
		print("Going Forward")
		
        	if(dis>1 and gps_flag==0):
            		z_angular=0
            		x_linear=7
		elif(gps_flag==1 and arrow_final_flag ==0):
			z_angular=0
            		x_linear=7
	
    	
	if(z_angular!=0):
        	out.twist.angular.z=z_angular
        	out.twist.linear.x=0
		
	else:
		out.twist.angular.z=0
        	out.twist.linear.x=x_linear

	
	if(gps_flag==1):

		print("GOAL REACHED SUCCESSFULLY!!!!!!!")


	pub.publish(out)	


def gps_callback(msg,pub):
	global x
	global y
	global dis
	global angle_to_goal
	global gps_flag
	global z_angular
	global arrow_final_flag,angle_by_arrow
	global theta

	x = msg.position.x
	y =msg.position.y

	x=-x
	y=-y

	
	dis = ((x*x)+(y*y))

	dis=sqrt(dis)
	print("************")		

	if(dis<1):
		print("GOAL REACHED SUCCESSFULLY!!!!!!!")
		gps_flag=1
	if(gps_flag == 0):

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
		
	elif(gps_flag==1 and arrow_final_flag == 1):
		angle_to_goal = angle_by_arrow

	else :
		angle_to_goal = angle_by_arrow
	if(z_angular!=0):
		out.twist.angular.z=z_angular
		out.twist.linear.x=0
	else:
		out.twist.angular.z=0
		out.twist.linear.x=x_linear
	
	pub.publish(out)

def arrow_callback(msg,pub):
	global arrow_final_flag,angle_by_arrow
	arrow_final_flag = msg.flag
	angle_by_arrow = msg.angle

def obstacle_callback(msg):
	global obstacle_flag,gps_flag
	obstacle_flag = msg.status
	if(obstacle_flag==2):
		gps_flag=1


if __name__ =='__main__' :
	rospy.init_node("speed_controller")
	pub = rospy.Publisher("/path_by_gps", Decider, queue_size = 1)
	sub1 = rospy.Subscriber("/distance", Pose, gps_callback,pub)
	sub4= rospy.Subscriber("/path_by_obstacle",Decider,obstacle_callback)
	sub2 = rospy.Subscriber("/imu_degree", Float64,imu_callback,pub)
	sub3 = rospy.Subscriber("/arrow",Arrow_feedback,arrow_callback,pub)
	rospy.spin()
