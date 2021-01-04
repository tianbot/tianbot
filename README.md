[中文版说明](https://github.com/tianbot/tianbot/blob/master/README_CN.md)  

[Tianbot详细中文操作手册](http://doc.tianbot.com/tianbot_omni)  

# Tianbot
Tianbot is a series of robots developed based on DJI RoboMaster board, motor and contoller. The typical design is a mecanum-wheeled robot with omni-directional movement. Moreover, differetial drive and ackermann steering geometry like a mars-rover are also supported.   

## Introduction
[Tianbot ROS Wiki](https://wiki.ros.org/tianbot)
Our goal is to develop a platform can be customized easily and the code can be deployed without any modification.

## Purchase from Tianbot Official Taobao Store

Tianbot platform can be ordered from out online shop. However, this platform is mainly for customization.
 
[点击这里进入淘宝购买或咨询客服： Purchase from Taobao:](https://item.taobao.com/item.htm?id=615976514264)  


## Specifications 

Customized

# Instructions
## Installation

```
cd ~/catkin_ws/src/
git clone https://github.com/tianbot/tianbot.git
cd ~/catkin_ws && catkin_make
```

## Interfacing
Tianbot can be brought up all at once, or separately.
```
roslaunch tianbot_bringup tianbot_bringup.launch
```
### Tianbot Base
```
roslaunch tianbot_core tianbot_core.launch
```

### Lidar
```
roslaunch tianbot_bringup lidar.launch
```

### RGBD Camera (if applicable)
```
roslaunch tianbot_bringup rgbd_camera.launch
```

### USB Camera
```
roslaunch tianbot_bringup usb_cam.launch
```

### GPS (if applicable)
```
roslaunch tianbot_bringup gps.launch
```

## Mapping
After bringing up the Tianbot, we provide three methods to perform slam for 2D laser.

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
### Save the Map
Map will be saved as tianbot_office in tianbot_slam/maps/
```
roslaunch tianbot_slam map_save.launch
```

## Navigation
After saving the map, the map can be used to perform navigation.
```
roslaunch tianbot_navigation tianbot_nav.launch
```
Configure running ROS across multiple machines, then launch rviz in a PC with display
```
roslaunch tianbot_rviz view_nav_amcl.launch
```

# License: BSD 3-Clause

