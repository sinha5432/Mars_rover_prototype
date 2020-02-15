#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from msg_pkg.msg import Decider_gps
from msg_pkg.msg import Decider


out=Twist()

obstacle_status=0
gps_status=0
goal_status=0
ball_status=0

gps_linear=0
gps_angular=0

obstacle_linear=0
obstacle_angular=0

ball_linear=0
ball_angular=0

counter=0
gps_reach=0
def stage_2():
	global obstacle_status
	global gps_status
	global ball_status
	global gps_linear
	global gps_angular
	global obstacle_linear
	global obstacle_angular
	global ball_linear
	global ball_angular
	global counter
	global gps_reach
	if (ball_status == 0 ):
		if(obstacle_status==1 and gps_status==0):
			out.linear.x=obstacle_linear
			out.angular.z=obstacle_angular
			print("avoiding_obstacle")
			counter=1

		elif(gps_status==0 and obstacle_status==0):
			if(counter>0 and counter<10):
				out.linear.x=6
				out.angular.z=0
				counter+=1
				print("avoiding_obstacle_fwd")
				print(counter)
			else:
				out.linear.x=gps_linear
				out.angular.z=gps_angular
				counter=0
				print("following goal")
		elif(gps_status==1):
			out.linear.x=ball_linear
			out.angular.z=ball_angular
			print("Goal Reached,finding ball")
			
	elif(ball_status == 1 and gps_reach==0):
		if(obstacle_status==1 and gps_status==0):
			out.linear.x=obstacle_linear
			out.angular.z=obstacle_angular
			print("avoiding_obstacle")
			counter=1

		elif(gps_status==0 and obstacle_status==0):
			if(counter>0 and counter<10):
				out.linear.x=6
				out.angular.z=0
				counter+=1
				print("avoiding_obstacle_fwd")
				print(counter)
			else:
				out.linear.x=gps_linear
				out.angular.z=gps_angular
				counter=0
				print("following goal")
		elif(gps_status==1):
			out.linear.x=ball_linear
			out.angular.z=ball_angular
			print("Goal Reached,finding ball")



	else:
		out.linear.x=ball_linear
		out.angular.z=ball_angular
		print("Following Ball")
	pub.publish(out)



def callback_obstacle(msg,pub):
	global obstacle_status
	global gps_status
	global ball_status
	global gps_linear
	global gps_angular
	global obstacle_linear
	global obstacle_angular
	global ball_linear
	global ball_angular
	global counter
	global gps_reach


	obstacle_status=msg.status
	obstacle_linear=msg.twist.linear.x
	obstacle_angular=msg.twist.angular.z

	stage_2()



def callback_gps(msg,pub):
	global obstacle_status
	global gps_status
	global ball_status
	global gps_linear
	global gps_angular
	global obstacle_linear
	global obstacle_angular
	global ball_linear
	global ball_angular
	global counter
	global gps_reach

	gps_status=msg.status
	gps_linear=msg.twist.linear.x
	gps_reach=msg.reach_flag
	gps_angular=-1*msg.twist.angular.z

	stage_2()



def callback_ball(msg,pub):
	global obstacle_status
	global gps_status
	global ball_status
	global gps_linear
	global gps_angular
	global obstacle_linear
	global obstacle_angular
	global ball_linear
	global ball_angular
	global counter
	global gps_reach

	ball_linear=msg.twist.linear.x
	ball_angular=msg.twist.angular.z
	ball_status=msg.status
	stage_2()
	




if __name__ == '__main__':
	rospy.init_node('path_decider')
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
	sub1 = rospy.Subscriber('/path_by_obstacle',Decider,callback_obstacle,pub)
	sub2 = rospy.Subscriber('/path_by_gps',Decider_gps,callback_gps,pub)
	sub3 = rospy.Subscriber('/path_by_ball',Decider,callback_ball,pub)

	rospy.spin()
