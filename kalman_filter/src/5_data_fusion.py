import rospy
from kalman_filter.msg import data_fusion
from geometry_msgs.msg import Pose
from kalman_filter.msg import vel_acc_msgs
from kalman_filter.msg import covarience_values

out = data_fusion()
px_e = py_e = 0
pxc = pyc = 0
n = 0

def center_point(msg):
    global pxc , pyc , n
    pxc, pyc = msg.x , msg.y
    n = n+1

def callback_encoder(msg):
    global n,px,py
    if(n):
        px = msg.px_e
        py = msg.py_e

def callback_gps(msg,pub):
    global px,py,out,n,pxc,pyc
    if(n):

        pxg , pyg = msg.position.x - pxc ,msg.position.y - pyc
        out.mx ,out.my = (pxg + px)/2 , (pyg + py)/2
        print(out)
        pub.publish(out)


if __name__ == '__main__':
    rospy.init_node("Data_fusion")
    pub = rospy.Publisher("/data_fusion",data_fusion,queue_size=1)
    sub = rospy.Subscriber("/covarience_matrix",covarience_values,center_point)
    sub1 = rospy.Subscriber("/distance",Pose,callback_gps,pub)
    sub2 = rospy.Subscriber("/vel_acc_pos",vel_acc_msgs,callback_encoder)
    rospy.spin()
