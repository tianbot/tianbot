#!/usr/bin/env python
#coding=utf-8

import rospy
#import time
#import thread
#import os  
import math
from geometry_msgs.msg import *
#from geometry_msgs.msg import Twist
#from nav_msgs.msg import *
#from nav_msgs.msg import Odometry
#import pyKDL
from visualization_msgs.msg import Marker

DISTANCE = 1.0 #m

class QRcode:
  def __init__(self):
    rospy.init_node('qrcode_controller_node', anonymous = True)
    self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 10)
    #self.nowpose_sub_ = rospy.Subscriber("odom", Odometry, self.getodomcb);#参数设置命令监听
    self.qrcode_sub_ = rospy.Subscriber("/visualization_marker", Marker, self.getqrcodecb);#参数设置命令监听
    self.rate = rospy.Rate(100)

    self.init_data()
    self.qr_controller_cyc()

  def init_data(self):
    #k
    self.ky = 1
    self.kx = -1
    self.kr = -2

    self.toleratex = 0.05
    self.toleratey = 0.05
    self.tolerateyaw = 0.02
    
    #max_vel
    self.maxvely = 0.5
    self.maxvelx = 0.5
    self.maxvelyyaw = 1

    self.tw = Twist()
    self.odom_targetyaw = 0
    self.odom_targetx = 0
    self.odom_targetz = DISTANCE

        
  def qr_controller_cyc(self):
    while not rospy.is_shutdown():
      #self.pub.publish(self.tw)
      self.rate.sleep()

  def col_vel(self,x,z,yaw):
    deltax = (self.odom_targetx - x)
    deltaz = (self.odom_targetz - z)
    deltayaw = (self.odom_targetyaw - yaw)
    
    if(abs(deltax) < self.toleratex):
      deltax = 0
    if(abs(deltaz) < self.toleratey):
      deltaz = 0
    if(abs(deltayaw) < self.tolerateyaw):
      deltayaw = 0 

    deltax = deltax * self.ky
    deltaz = deltaz * self.kx
    deltayaw = deltayaw * self.kr

    if(abs(deltax) > self.maxvely):
      deltax = self.maxvely
    if(abs(deltaz) > self.maxvelx):
      deltaz = self.maxvelx
    if(abs(deltayaw) > self.maxvelyyaw):
      deltayaw = self.maxvelyyaw

    self.tw.linear.y = deltax
    self.tw.linear.x = deltaz
    self.tw.angular.z = deltayaw
    self.pub.publish(self.tw)

  def getqrcodecb(self,qrcodedata):
    x = qrcodedata.pose.position.x
    z = qrcodedata.pose.position.z
    angle = qrcodedata.pose.orientation.z
    self.col_vel(x,z,angle)

  def quat_to_angle(self,quat):
    #rot = PyKDL.Rotation.Quaternion(quat.x, quat.y, quat.z, quat.w)
    #return rot.GetRPY()[2]
    x=quat.x
    y=quat.y
    z=quat.z
    w=quat.w

    r = math.atan2(2*(w*x+y*z),1-2*(x*x+y*y))
    p = math.asin(2*(w*y-z*z))
    y = math.atan2(2*(w*z+x*y),1-2*(z*z+y*y))

    angleR = r*180/math.pi
    angleP = p*180/math.pi
    angleY = y*180/math.pi  

    return angleY,angleP,angleR

if __name__ == '__main__':
    try:
      qrcode = QRcode()
    except rospy.ROSInterruptException as e:
      print e


