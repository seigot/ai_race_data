#!/bin/bash -x

echo "start prepare.sh"

gnome-terminal -e "python3 judgeServer.py"
sleep 1
gnome-terminal -e "python3 timer.py"

#roslaunch user_tutorial2 wheel_robot.launch
