#!/usr/bin/env python
#coding=utf-8

#####################################
# 程序说明
# 1，小车能识别各种二维码
# 2，当小车识别到一个二维码后，运动到二维码一定目标位置
# 3，当小车运动完成后，就不在响应上次二维码的位置识别了，逆时针旋转寻找另外的二维码
# 4，在小车未达到目标位置的过程中，二维码在视野丢失，小车并不会能自转寻找二维码，即停在原地

###################################

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
from ar_track_alvar_msgs.msg import AlvarMarkers

DISTANCE = 0.5 #相机与二维码保持的目标距离

#定义了一个QRcode的类
class QRcode:
  def __init__(self):#相当于构造函数，实例化需要运行的函数
    rospy.init_node('qrcode_controller_node', anonymous = True)#初始化ros节点
    self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 10)#发布速度信息，'/cmd_vel'为话题，Twist为消息类型，queue_size为消息栈长度
    self.qrcode_sub_ = rospy.Subscriber("/ar_pose_marker", AlvarMarkers, self.getqrcodecb);#监听识别的二维码信息话题，"/ar_pose_marker"为话题名，AlvarMarkers为消息类型，self.getqrcodecb为收到消息进入的回调函数
    self.rate = rospy.Rate(100)#定义延期，100hz，时间为10ms，此程序没有使用

    self.init_data() #数据初始化函数
    self.qr_controller_cyc() #死循环，此处循环没有干任何事，主要事不让程序退出，阻塞用，等待回调

  def init_data(self):
    print("init_data")
    #k，大小表示增益，符号表示camera_link和base_link各对应轴之间的方向，见程序计算过程
    self.ky = 0.8#增益 
    self.kx = -0.7
    self.kr = -2

    self.signed = 1 #防止二维码倒置

    #允许目标的误差范围，单位m,rad
    self.toleratex = 0.05
    self.toleratey = 0.05
    self.tolerateyaw = 0.02
    
    #允许控制的最大小车速度，单位m,rad
    self.maxvely = 0.3
    self.maxvelx = 0.3
    self.maxvelyyaw = 1

    #初始化发布小车控制消息
    self.tw = Twist()

    #是否到达目标位置的标志，到达后才能选装，中途丢掉目标不旋转
    self.arrived = 0
    self.spinYaw = 0.3 #旋转的角速度
    self.qrcodeNum_now = -1
    self.qrcodeNum_last = -1 #正在或者上一个识别的二维码标签，下次就不跟踪了

    #设定相机与二维码的相对位置，作为跟踪的目标值，以camera_link为坐标系
    self.odom_targetyaw = 0 #垂直方向，可以不设，程序中不做判断
    self.odom_targetx = 0 #水平方向（车辆左右方向），正中心
    self.odom_targetz = DISTANCE # 车辆前后方向，距离1m

        
  def qr_controller_cyc(self):
    while not rospy.is_shutdown(): #主循环，阻塞作用
      if(self.arrived == 1):#在到达目标后才开始旋转，中途失掉目标不旋转
        self.tw.linear.y = 0
        self.tw.linear.x = 0 
        self.tw.angular.z = 0.3
        self.pub.publish(self.tw)
      self.rate.sleep()


#基坐标和相机坐标个方向的对应关系
#  基坐标          相机坐标
#   Xo +  <---->    Zc +
#   Yo +  <---->    Xc -
#   Zo +  <---->    Yc -

  def col_vel(self,x,z,yaw):
    deltax = (self.odom_targetx - x)  #目标值x与当前值做差，，，都是相对位置，，坐标系camera_link
    deltaz = (self.odom_targetz - z)  #目标值z与当前值做差，，，都是相对位置，，坐标系camera_link
    deltayaw = (self.odom_targetyaw - yaw)  #目标值"yaw"与当前值做差，，，都是相对位置，，坐标系camera_link
    
    # 判断如果差值小于位置误差允许的范围，表示已经到达，直接赋差值为0
    if(abs(deltax) < self.toleratex): 
      deltax = 0
    if(abs(deltaz) < self.toleratey):
      deltaz = 0
    if(abs(deltayaw) < self.tolerateyaw):
      deltayaw = 0 

    #deltax，deltaz，deltayaw是在camera_link下的差值，此时通过ky,kz,kr的符号开反向，大小来表示最后的控制增益，结果直接作为控制小车的速度
    deltax = deltax * self.ky   #base_link的y方向（左右方向）,camera_link的x方向
    deltaz = deltaz * self.kx  #base_link的x方向（左右方向），camera_link 的z方向
    deltayaw = deltayaw * self.kr #base_link的yaw方向（左右方向），camera_link 的z方向

    #限制控制速度，不超出设置范围
    if(deltax > self.maxvely):
      deltax = self.maxvely
    elif (deltax < -self.maxvely):
      deltax = -self.maxvely
    if(deltaz > self.maxvelx):
      deltaz = self.maxvelx
    elif(deltaz < -self.maxvelx):
      deltaz = -self.maxvelx
    if(deltayaw > self.maxvelyyaw):
      deltayaw = self.maxvelyyaw
    elif(deltayaw < -self.maxvelyyaw):
      deltayaw = -self.maxvelyyaw

    #得出的三个控制量，base_link下的x,y,yaw，赋值并发送话题
    if(deltax == 0 and deltaz==0 and deltayaw==0):
      self.qrcodeNum_last = self.qrcodeNum_now
      self.arrived = 1
    else:
      self.arrived = 0

    self.tw.linear.y = deltax * self.signed
    self.tw.linear.x = deltaz 
    self.tw.angular.z = deltayaw* self.signed
    self.pub.publish(self.tw)

  def getqrcodecb(self,qrcodedatas):
    #print('into cb') #如果收到话题消息，调试用
    qrcodedatalist =  qrcodedatas.markers
    for qrcodedata in qrcodedatalist:
      if(not qrcodedata.id == self.qrcodeNum_last):
        #print("id:%s" % (qrcodedata.id))
        self.qrcodeNum_now = qrcodedata.id
        x = qrcodedata.pose.pose.position.x #二维码位姿，相对于相机坐标的x值
        z = qrcodedata.pose.pose.position.z #二维码位姿，相对于相机坐标的z值,相机y轴为垂直方向，此处不用
        angle = qrcodedata.pose.pose.orientation.z#二维码姿态，相对于相机坐标的四元数中的z值

        #防止二维码倒放导致的勿跟踪
        try:
          an = self.quat_to_angle(qrcodedata.pose.pose.orientation)
          yaw = an[0]
          if(yaw < -90 or yaw > 90):
            self.signed = 0
          else:
            self.signed = 1
        except Exception as e:
          print(e)
        #print("roll:%s,pitch:%s,yaw:%s" % (an[2],an[1],an[0]))#调试用
        self.col_vel(x,z,angle)#利用相对于相机的二维码位置，来计算相对于车基坐标的位置，相机和车基坐标存在变换关系 


  #四元素转欧拉角，此程序没有使用，忽略
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
    #return angleR


  #程序入口，相当于main函数
if __name__ == '__main__':
    try:
      qrcode = QRcode() #实例化QRcode对象
    except rospy.ROSInterruptException as e:
      print e


