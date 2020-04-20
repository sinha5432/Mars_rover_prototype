#!/usr/bin/env python
import rospy
import numpy as np
import time
from kalman_filter.msg import covarience_values        ##covarience values message type i.e. sx,sy,x,y
from kalman_filter.msg import kalman_filtered_values   ## kalman_filtered_values i.e final.x,final.y
from geometry_msgs.msg import Pose                     ##takes values from distance topic i.e. gps_data_conversion filer
from kalman_filter.msg import vel_acc_msgs             ##gives values of vx,ax,vy,ay,px,py
import math
from kalman_filter.msg import data_fusion             ##gives values of vx,ax,vy,ay,px,py


n = 0
flag = 0.0 ## calculation will not start until covarience values are got
ax = 0.0
ay = 0.0
dt = 1
previous_time = 0
theta = 0
std_x = std_y = 0.0
i = 0.0   ## used for first time calculation and becomes 1 after first calculation
px = 0.0
py = 0.0
xc = 0
yc = 0
std_vx=0
std_vy=0
px=0
py=0
final = kalman_filtered_values()
X = []
P = []
R = []
A = []
B = []
U = []
Q = []
Y = []
K = []

def kf_predict():
    global X,P,A,B,U,Q,dt,theta,Y
    X =  np.dot(A,X) + np.dot (B,U)
    P = np.dot(A, np.dot(P,A.T)) + Q

def kf_update():
    global X,P,Y,H,R,dt,theta ,Y
    IM = np.dot(H,X)
    IS = R + np.dot(H,np.dot(P,H.T))
    K = np.dot(P , np.dot(H.T , np.linalg.inv(IS)))
    X = X + np.dot(K , (Y - IM))
    P = P- np.dot(K , np.dot(IS,K.T))


def intialization():
    global A,B,H,Q,P,X,U,R,dt,theta,px,py,Y
    A = np.array([[1.0, 0.0, dt , 0.0],
                 [0.0, 1.0, 0.0, dt],
                 [0.0, 0.0, 1.0, 0],
                 [0.0, 0.0, 0.0,1.0]])
    B = np.array([[(0.5)*(dt**2) , 0.0],
                [0.0 , (0.5)*(dt**2) ] ,
                [ dt , 0.0] ,
                [ 0.0, dt]])

    H = np.array([[1,0,0,0],
                [0,1,0,0]])

    Q = (std_acc)* np.array([[(0.25)*(dt**4) , 0.0 , (0.5)*(dt**3) , 0.0] ,
                [0.0 , (0.25)*(dt**4) , 0.0 , (0.5)*(dt**3)] ,
                [ (0.5)*(dt**3) , 0.0 , (dt**2) , 0.0] ,
                [ 0.0 , (0.5)*(dt**3) , 0.0 , (dt**2)]])

    P = np.diag((std_x**2, std_y**2, std_vx**2, std_vy**2))

    X = np.array([[0],
                [0],
                [0],
                [0.0]])

    U = np.array([[ax] ,
                [ay]])

    R = np.diag((std_x,std_y))

    Y = np.array([[px],[py]])

def flagback(msg):
    global flag,std_x,std_y,std_vx,std_vy,std_acc,dt,previous,theta,Y
    std_x = msg.sx
    std_y = msg.sy
    std_vx = msg.svx
    std_vy = msg.svy
    std_acc = msg.sacc
    flag =1

def vel_acc_callback(msg):
    if flag == 1:
        global ax,ay,theta
        ax = msg.ax_e
        ay = msg.ay_e
        theta =msg.theta


def fusion_callback(msg , pub):
    if flag == 1:
        global final ,dt,previous_time,n,theta, Y,px,py,pxm,pym
        global A,B,H,Q,P,X,U,R
        if n <= 1:
            dt = 1
        else:
            dt = time.time() - previous_time
        previous_time = time.time()
        px = msg.mx
        py = msg.my
        intialization()
        kf_predict()
        kf_update()
        print(X)
        final.x = X[0][0]
        final.y = X[2][0]
        n = n+1
        pub.publish(final)


if __name__ == '__main__':
    rospy.init_node('kalman_logic')
    pub = rospy.Publisher('filtered_distance' , kalman_filtered_values, queue_size = 5)
    sub = rospy.Subscriber('covarience_matrix' , covarience_values , flagback)
    sub1 = rospy.Subscriber('vel_acc_pos' , vel_acc_msgs , vel_acc_callback)
    sub2 = rospy.Subscriber('data_fusion' , data_fusion , fusion_callback , pub)
    rospy.spin()
