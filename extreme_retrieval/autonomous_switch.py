#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Pose
from math import atan2
from math import sqrt
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist


x = 0.0
y = 0.0
x_linear=0
angle_to_goal = 0.0
p_error=0
z_angular=0
dis = 1000

gps_flag=0


out=Twist()


def callback(msg,pub):

	global angle_to_goal
	global p_error
	global z_angular
	global x_linear
	global gps_flag

	theta = msg.data
	print("{}distance to goal".format(dis))
	print("{}flag ".format(gps_flag))
	error=angle_to_goal-theta
	#print("error")
	#print(error)
	if(error>180):
		error=error-360
	if(error<-180):
		error=error+360
	kp=0.2
	

	if(dis<1):
		print("GOAL REACHED SUCCESSFULLY!!!!!!!")
		gps_flag=1

        if(error>10 or error<-10):
        	z_angular=kp*error
		print(kp*error)
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
            		x_linear=9
        	else:
			z_angular=0
            		x_linear=0
	
    	
	if(z_angular!=0):
        	out.angular.z=z_angular
        	out.linear.x=0
		
	else:
		out.angular.z=0
        	out.linear.x=x_linear

	
	if(gps_flag==1):
		out.angular.z=0
		out.linear.x=0
		pub.publish(out)
		print("GOAL REACHED SUCCESSFULLY!!!!!!!")
	

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
	print("************")		
	#print("{}Angle to goal".format(angle_to_goal))		
	#print("{}distance to goal".format(dis))
	
	if(gps_flag==1):
		out.angular.z=0
		out.linear.x=0
		print("GOAL REACHED SUCCESSFULLY!!!!!!!")

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

	if(z_angular!=0):
		out.angular.z=z_angular
		out.linear.x=0
	else:
		out.angular.z=0
		out.linear.x=x_linear
		
	pub.publish(out)





if __name__ =='__main__' :

	rospy.init_node("speed_controller")
	pub = rospy.Publisher("/cmd_vel_autonomous", Twist, queue_size = 1)
	sub1 = rospy.Subscriber("/distance", Pose, newOdom,pub)
	sub2 = rospy.Subscriber("/imu_degree", Float64,callback,pub)
	rospy.spin()
