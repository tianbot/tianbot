#!/bin/bash

echo "Tianbot Udev Rules Updating..."
echo "Check it using the command : ls -l /dev | grep tianbot"

sudo cp -f ./_udev_/*.rules  /etc/udev/rules.d

echo " "
echo "Restarting udev"
echo ""
sudo service udev reload
sudo service udev restart

echo "Finish. "
