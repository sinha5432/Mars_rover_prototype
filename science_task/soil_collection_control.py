#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
from msg_pkg.msg import manipulator


m = manipulator()
def joystick_cb(msg, manipulator_pub):


	#stop code
	if (msg.buttons[6]==1):  
		m.motor_1_pwm=0
		#m.motor_2_pwm=0
		m.motor_3_pwm=0
		m.motor_4_pwm=0
		#m.motor_5_pwm=0
		m.motor_6_pwm=0
		manipulator_pub.publish(m)

	########## motor 1 #########

	elif (msg.buttons[0]==1 and msg.axes[6]==1):
		m.motor_1_pwm=255
		#m.motor_2_pwm=0
		m.motor_3_pwm=0
		m.motor_4_pwm=0
		#m.servo_position=0
		m.motor_6_pwm=0
		manipulator_pub.publish(m)

	elif (msg.buttons[0]==1 and msg.axes[6]==-1):
		m.motor_1_pwm=-255
		#m.motor_2_pwm=0
		m.motor_3_pwm=0
		m.motor_4_pwm=0
		#m.servo_position=0
		m.motor_6_pwm=0
		manipulator_pub.publish(m)

	
	########## motor 3 #########

	elif (msg.buttons[2]==1 and msg.axes[6]==1):
		m.motor_1_pwm=0
		#m.motor_2_pwm=0
		m.motor_3_pwm=100
		m.motor_4_pwm=0
		#m.servo_position=0
		m.motor_6_pwm=0
		manipulator_pub.publish(m)

	elif (msg.buttons[2]==1 and msg.axes[6]==-1):
		m.motor_1_pwm=0
		#m.motor_2_pwm=0
		m.motor_3_pwm=-100
		m.motor_4_pwm=0
		#m.servo_position=0
		m.motor_6_pwm=0
		manipulator_pub.publish(m)

	########## motor 4 #########

	elif (msg.buttons[3]==1 and msg.axes[6]==1):
		m.motor_1_pwm=0
		#m.motor_2_pwm=0
		m.motor_3_pwm=0
		m.motor_4_pwm=100
		#m.servo_position=0
		m.motor_6_pwm=0
		manipulator_pub.publish(m)

	elif (msg.buttons[3]==1 and msg.axes[6]==-1):
		m.motor_1_pwm=0
		#m.motor_2_pwm=0
		m.motor_3_pwm=0
		m.motor_4_pwm=-100
		#m.servo_position=0
		m.motor_6_pwm=0
		manipulator_pub.publish(m)

	

	########## motor 6 #########

	elif (msg.buttons[7]==1 and msg.axes[6]==1):
		m.motor_1_pwm=0
		#m.motor_2_pwm=0
		m.motor_3_pwm=0
		m.motor_4_pwm=0
		#m.servo_position=0
		m.motor_6_pwm=150
		manipulator_pub.publish(m)

	elif (msg.buttons[7]==1 and msg.axes[6]==-1):
		m.motor_1_pwm=0
		#m.motor_2_pwm=0
		m.motor_3_pwm=0
		m.motor_4_pwm=0
		#m.servo_position=0
		m.motor_6_pwm=-255
		manipulator_pub.publish(m)
	
	########## motor 2 #########


	if (msg.buttons[1]==1 and msg.axes[6]==1):
		m.motor_2_pwm=255
		manipulator_pub.publish(m)

	elif (msg.buttons[1]==1 and msg.axes[6]==-1):
		m.motor_2_pwm=-255
		manipulator_pub.publish(m)
	elif(msg.buttons[8]==1):
		m.motor_2_pwm=0
		manipulator_pub.publish(m)
	

	########## motor 5 (servo) #########

	if (msg.buttons[5]==1 and msg.axes[6]==1):
		
		m.motor_5_pwm=m.motor_5_pwm+10
		if(m.motor_5_pwm>=180):
			m.motor_5_pwm=180
		elif(m.motor_5_pwm<0):
			m.motor_5_pwm=0
		manipulator_pub.publish(m)

	elif (msg.buttons[5]==1 and msg.axes[6]==-1):
		m.motor_5_pwm=m.motor_5_pwm-5
		if(m.motor_5_pwm>=180):
			m.motor_5_pwm=180
		elif(m.motor_5_pwm<0):
			m.motor_5_pwm=0
		manipulator_pub.publish(m)
	elif(msg.buttons[4]==1):
		if(m.motor_5_pwm>0):
			m.motor_5_pwm=0
		else:
			m.motor_5_pwm=45
		
		manipulator_pub.publish(m)
	print m;
	print("**********")




if __name__ == '__main__':
	rospy.init_node('manipulator_joystick')
	manipulator_pub = rospy.Publisher('soil_collection',manipulator,queue_size=50)
	rospy.Subscriber('joy',Joy,joystick_cb, manipulator_pub)
	rospy.spin()
