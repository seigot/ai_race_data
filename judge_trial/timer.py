## qt5
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys 
## http communication
import requests
from time import sleep
import json
import numpy as np
import cv2
import os
import copy
import datetime

class Window(QMainWindow): 
  
    def __init__(self): 
        super().__init__() 
  
        # setting title 
        self.setWindowTitle("Python Stop watch") 

        # setting geometry
        upper_left = (100,100)
        width_height = (400, 200)
        self.setGeometry(upper_left[0], upper_left[1],
                         width_height[0], width_height[1]) 

        # calling method 
        self.UiComponents() 

        # showing all the widgets 
        self.show() 

    # method for widgets 
    def UiComponents(self): 

        # timer parameter
        self.timer_count = 0.0
        self.timer_flag = True #False
        # LAP parameter
        self.lap_count = 0
        self.lap_count_max = 3

        # creating a label to show the time 
        self.label = QLabel(self)
        label_upper_left = (75, 20)
        label_width_height = (250, 100)
        self.label.setGeometry(label_upper_left[0], label_upper_left[1], 
                               label_width_height[0], label_width_height[1]) 
        self.label.setStyleSheet("border : 4px solid black;") 
        self.label.setText(self.gettimertext())
        self.label.setFont(QFont('Arial', 25))
        self.label.setAlignment(Qt.AlignCenter) 
  
        # create start button 
        start = QPushButton("Start", self) 
        start_upper_left = (15, 150)
        start_width_height = (90, 40)
        start.setGeometry(start_upper_left[0], start_upper_left[1], 
                          start_width_height[0], start_width_height[1])
        start.pressed.connect(self.Start) 

        # create pause button
        pause = QPushButton("Pause", self) 
        pause_upper_left = (110, 150)
        pause_width_height = (90, 40)
        pause.setGeometry(pause_upper_left[0], pause_upper_left[1],
                          pause_width_height[0], pause_width_height[1])
        pause.pressed.connect(self.Pause) 
  
        # create reset button 
        reset = QPushButton("Reset", self) 
        reset_upper_left = (205, 150)
        reset_width_height = (90, 40)
        reset.setGeometry(reset_upper_left[0], reset_upper_left[1],
                          reset_width_height[0], reset_width_height[1])
        reset.pressed.connect(self.Reset) 

        # create lap_count button 
        lapcount = QPushButton("LapCount", self) 
        lapcount_upper_left = (300, 150)
        lapcount_width_height = (90, 40)
        lapcount.setGeometry(lapcount_upper_left[0], lapcount_upper_left[1],
                             lapcount_width_height[0], lapcount_width_height[1])
        lapcount.pressed.connect(self.LapCount) 
  
        # creating a timer object 
        timer = QTimer(self) 
        timer.timeout.connect(self.callback_showTime)
        timer.start(100) # update the timer by n(msec)

    # timer callback function 
    def callback_showTime(self):
        # check lap count
        if self.lap_count >= self.lap_count_max:
            self.timer_flag = False

        # update timer_conut
        if self.timer_flag == True:
            self.timer_count+= 1

        # showing text 
        self.label.setText(self.gettimertext())
  
    # start button
    def Start(self):
        self.timer_flag = True

    # pause button
    def Pause(self):
        self.timer_flag = False

    # reset button
    def Reset(self):
        self.timer_flag = False
        self.timer_count = 0
        self.lap_count = 0
        self.label.setText(self.gettimertext())

    # lap count button
    def LapCount(self):
        self.lap_count += 1
        self.label.setText(self.gettimertext())

    def gettimertext(self):

        # request data to server
        data = self.urlreq()
        time = data["judge_info"]["time"]
        lap_count = data["judge_info"]["lap_count"]

        passed_time_str = str('{:.2f}'.format(time))
        lap_count_str = str(lap_count)
        lap_count_max_str = str(self.lap_count_max)
        #passed_time = str('{:.01f}'.format(self.timer_count / 10)) + " (s)" + "\n" + "LAP: " + str(self.lap_count)
        #lap_count_str = str(self.lap_count_max)

        # time text
        text = "TIME: " + passed_time_str + " (s)" + "\n" + "LAP: " + lap_count_str  + "/" + lap_count_max_str

        return text

    def urlreq(self):
        resp = requests.get("http://localhost:5000/raceState")
        data = json.loads(resp.text)
        #time = data["judge_info"]["time"]
        #lap_count = data["judge_info"]["lap_count"]
        #print(str('{:.2f}'.format(time)) + " " + str(lap))

        return data


# create pyqt5 app 
App = QApplication(sys.argv) 
  
# create the instance of our Window 
window = Window() 
  
# start the app 
sys.exit(App.exec()) 
