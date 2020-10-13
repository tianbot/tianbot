# Set some defaults to tianbot launch environment

: ${TIANBOT_BASE:=tianbot_omni}  #tianbot_omni, tianrover, tianbot_mini.
: ${TIANBOT_BASE_MODEL:=06q1}  #06q1, 06q2, 08q1, 08q2, 08q8, etc
: ${TIANBOT_BASE_PORT:=/dev/tianbot_base}  # /dev/ttyUSB1
: ${TIANBOT_RGBD_CAMERA:=none} #realsense_d415, realsense_d435, astra, astra_pro, xtion, none 
: ${TIANBOT_VIDEO_DEVICE:=none} # /dev/video0 for most of the usb_cams.If you want init usb_cam in jet_cam, this should be set to none.
#/dev/video2 if using realsense, none
: ${TIANBOT_LIDAR:=osight_lidar} # rplidar_a1, rplidar_a2, rplidar_a3, osight_lidar, velodyne_vlp16
: ${TIANBOT_LIDAR_MODEL:=iexxx} # lidar model. a1, a2, a3 for rplidar. iexxx and ie303 for osight. vlp16 for velodyne, etc. 
: ${TIANBOT_LIDAR_IP:=192.168.1.10} # lidar ip, used for velodyne, RoboSense, Osight, hokuyo, etc. 
: ${TIANBOT_LIDAR_PORT:=/dev/osight_lidar} # /dev/ttyUSB0 
: ${TIANBOT_GPS:=none} # none, nmea0183
: ${TIANBOT_JOY_MODE:=X} # logitech joy mode X, D


#Exports
export TIANBOT_BASE
export TIANBOT_BASE_MODEL
export TIANBOT_BASE_PORT
export TIANBOT_RGBD_CAMERA
export TIANBOT_VIDEO_DEVICE
export TIANBOT_LIDAR
export TIANBOT_LIDAR_MODEL
export TIANBOT_LIDAR_IP
export TIANBOT_LIDAR_PORT
export TIANBOT_GPS
export TIANBOT_JOY_MODE
