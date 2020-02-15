import rospy
from msg_pkg.msg import Arrow_feedback,Arrow_detection
from msg_pkg.msg import Decider
from std_msgs.msg import Float64
import time
angle = 0
arrow_final_flag = 0
final = Arrow_feedback()
angle_by_arrow=0
arrow_final_flag=0
x_linear=z_angular=0
n=0
diff = 0
count = 0
obstacle_flag = 0
ocount=0
def finding_arrow():
	global x_linear,z_angular,arrow_final_flag 
	x_linear = 0
	z_angular = -3
	final.x_linear = x_linear
	final.z_angular = z_angular
	arrow_final_flag = 0
def left():
	global x_linear,z_angular
	x_linear = 0
	z_angular = -5
	final.x_linear = x_linear
	final.z_angular = z_angular
def right():
	global x_linear,z_angular
	x_linear = 0
	z_angular = 5
	final.x_linear = x_linear
	final.z_angular = z_angular
def stop():
	global x_linear,z_angular,arrow_final_flag 
	x_linear = 0
	z_angular = 0
	final.x_linear = x_linear
	final.z_angular = z_angular

def arrow_callback(msg,pub):
	global final,angle_by_arrow,n,angle,count,diff,obstacle_flag,ocount
	global arrow_final_flag
	detection = msg.detection
	direction = msg.direction
	centre = msg.x - 320


	if arrow_final_flag == 1 :
		diff = angle_by_arrow - angle
		if (diff > 180) :
			diff = diff -360
		else :
			diff=diff
			
		print("Setttttttttttttttttttttttttttttttttttttttttttttttttttttttt")
		if (diff <5 and diff >-5):
			arrow_final_flag = 0
			obstacle_flag = 1
			pub.publish(final)
		else:
			arrow_final_flag=1
			obstacle_flag = 0
	else :
		print("Setting")
		if detection == 1 :
			if (centre < 100 and centre >-100):
				if(direction == 1):
					if(n==0):
						angle_by_arrow = angle + 90
						n=1
						count+=1
						if(angle_by_arrow >=360):
							angle_by_arrow -=360
					else :
						angle_by_arrow = angle_by_arrow
					arrow_final_flag=1

				elif(direction == -1):
					if(n==0):
						angle_by_arrow = angle - 90
						n=1
						count+=1
						if(angle_by_arrow <=0):
							angle_by_arrow +=360
					else :
						angle_by_arrow = angle_by_arrow
					arrow_final_flag=1
				print("aligned")
				stop()
			elif (centre >100):
				left()
				arrow_final_flag = 0
				print("Left")
			else :
				right()
				arrow_final_flag = 0
				print("RIGHT")
		else :
			finding_arrow()
			time.sleep(0.5)
			pub.publish(final)
			stop()
			time.sleep(0.5)
			pub.publish(final)
			print("Finding Arrow")
		
		obstacle_flag = 0

	final.flag = arrow_final_flag
	final.angle = angle_by_arrow
	final.obstacle_flag = obstacle_flag
	#print(angle)
	#print(final)
	print(obstacle_flag)
	print("----------------------------------")
	pub.publish(final)

def imu_callback(msg):
	global angle
	angle = msg.data

if __name__ == "__main__" :
	rospy.init_node("Arrow")
	pub = rospy.Publisher("/arrow",Arrow_feedback , queue_size = 1)
	sub1 = rospy.Subscriber("/velocity", Arrow_detection, arrow_callback,pub)
	sub2 = rospy.Subscriber("/imu_degree", Float64,imu_callback)
	rospy.spin()
