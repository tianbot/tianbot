[English](https://github.com/tianbot/tianbot/blob/master/README.md)  

[Tianbot详细中文操作手册](http://doc.tianbot.com/tianbot_omni)  

# Tianbot
Tianbot全系列机器人。包括Tianbot Omni全向系列，四个轮子采用麦克纳姆轮对称布置、独立驱动。也支持Tianrover六轮阿克曼结构火星车底盘。也支持Tianbot差速机器人系列。
全系列机器人主要采用DJI机甲大师系列控制器、电机及其驱动器等，性能强劲，品质保证，对标Maxon电机，成本更低。

## 介绍
[Tianbot ROS Wiki](https://wiki.ros.org/tianbot)
Tianbot系列机器人不仅有标准平台，同时可以通过模块化设计进行快速设计，并且无需代码改动即可驱动。

## 购买

标准平台购买可以通过官方淘宝.
 
[点击这里进入淘宝购买或咨询客服： Purchase from Taobao:](https://item.taobao.com/item.htm?id=615976514264)  


## 参数 

因配置而异

# 使用
## 安装

```
cd ~/catkin_ws/src/
git clone https://github.com/tianbot/tianbot.git
cd ~/catkin_ws && catkin_make
```

## 通信
Tianbot可以一次全部启动,或者单独启动各个部件.
```
roslaunch tianbot_bringup tianbot_bringup.launch
```
### Tianbot 底盘
```
roslaunch tianbot_core tianbot_core.launch
```

### 激光雷达
```
roslaunch tianbot_bringup lidar.launch
```

### 深度相机 (if applicable)
```
roslaunch tianbot_bringup rgbd_camera.launch
```

### USB摄像头
```
roslaunch tianbot_bringup usb_cam.launch
```

### GPS (if applicable)
```
roslaunch tianbot_bringup gps.launch
```

## 建图
启动Tianbot后, 我们提供三种方式进行二维建图.

### GMapping
```
roslaunch tianbot_slam tianbot_gmapping.launch
```
### HectorSLAM
```
roslaunch tianbot_slam tianbot_hector.launch
```
### Cartographer
```
roslaunch tianbot_slam tianbot_cartographer.launch
```
### 保存地图
地图默认保存在tianbot_slam/maps/目录下，名称为tianbot_office
```
roslaunch tianbot_slam map_save.launch
```

## 导航
保存地图后，下列程序会使用默认地图进行导航.
```
roslaunch tianbot_navigation tianbot_nav.launch
```
如果正确配置了ROS的多机互联, 可以在控制台电脑上打开RViz进行查看
```
roslaunch tianbot_rviz view_nav_amcl.launch
```

# 开源协议: BSD 3-Clause
