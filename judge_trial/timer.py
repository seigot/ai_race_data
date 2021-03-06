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
import os
import datetime

JUDGESERVER_REQUEST_URL="http://127.0.0.1:5000/judgeserver/request"
JUDGESERVER_UPDATEDATA_URL="http://127.0.0.1:5000/judgeserver/updateData"
JUDGESERVER_GETSTATE_URL="http://127.0.0.1:5000/judgeserver/getState"

g_slidar = "aa"

class Window(QMainWindow): 
  
    def __init__(self): 
        super().__init__() 
  
        # setting title 
        self.setWindowTitle("Python Stop watch") 

        # setting geometry
        upper_left = (100,100)
        width_height = (600, 240)
        self.setGeometry(upper_left[0], upper_left[1],
                         width_height[0], width_height[1]) 

        # calling method 
        self.UiComponents() 

        # showing all the widgets 
        self.show() 

    # method for widgets 
    def UiComponents(self): 

        # creating a label to show the time 
        self.label = QLabel(self)
        label_upper_left = (20, 10)
        label_width_height = (560, 130)
        self.label.setGeometry(label_upper_left[0], label_upper_left[1], 
                               label_width_height[0], label_width_height[1]) 
        self.label.setStyleSheet("border : 4px solid black;") 
        self.label.setText(self.gettimertext())
        self.label.setFont(QFont('Arial', 25))
        self.label.setAlignment(Qt.AlignCenter) 
  
        # create start button 
        start = QPushButton("Init", self) 
        start_upper_left = (15, 150)
        start_width_height = (90, 40)
        start.setGeometry(start_upper_left[0], start_upper_left[1], 
                          start_width_height[0], start_width_height[1])
        start.pressed.connect(self.Init)

        # create pause button
        pause = QPushButton("Start", self) 
        pause_upper_left = (110, 150)
        pause_width_height = (90, 40)
        pause.setGeometry(pause_upper_left[0], pause_upper_left[1],
                          pause_width_height[0], pause_width_height[1])
        pause.pressed.connect(self.Start)

        # create reset button 
        reset = QPushButton("Stop", self) 
        reset_upper_left = (205, 150)
        reset_width_height = (90, 40)
        reset.setGeometry(reset_upper_left[0], reset_upper_left[1],
                          reset_width_height[0], reset_width_height[1])
        reset.pressed.connect(self.Stop)

        # create lap_count button 
        lapcount = QPushButton("Lap++", self) 
        lapcount_upper_left = (15, 195)
        lapcount_width_height = (90, 40)
        lapcount.setGeometry(lapcount_upper_left[0], lapcount_upper_left[1],
                             lapcount_width_height[0], lapcount_width_height[1])
        lapcount.pressed.connect(self.LapCount_plus) 

        lapcount = QPushButton("Lap--", self) 
        lapcount_upper_left = (110, 195)
        lapcount_width_height = (90, 40)
        lapcount.setGeometry(lapcount_upper_left[0], lapcount_upper_left[1],
                             lapcount_width_height[0], lapcount_width_height[1])
        lapcount.pressed.connect(self.LapCount_minus)

        # create courseout_count button 
        lapcount = QPushButton("CourseOut++", self) 
        lapcount_upper_left = (205, 195)
        lapcount_width_height = (90, 40)
        lapcount.setGeometry(lapcount_upper_left[0], lapcount_upper_left[1],
                             lapcount_width_height[0], lapcount_width_height[1])
        lapcount.pressed.connect(self.CourseOutCount_plus) 
        lapcount.setFont(QFont("Meiryo", 9))

        lapcount = QPushButton("CourseOut--", self) 
        lapcount_upper_left = (300, 195)
        lapcount_width_height = (90, 40)
        lapcount.setGeometry(lapcount_upper_left[0], lapcount_upper_left[1],
                             lapcount_width_height[0], lapcount_width_height[1])
        lapcount.pressed.connect(self.CourseOutCount_minus)
        lapcount.setFont(QFont("Meiryo", 9))

        # creating a timer object 
        timer = QTimer(self) 
        timer.timeout.connect(self.callback_showTime)
        timer.start(500) # update the timer by n(msec)

    def display_slider():
        print(g_slidar.value())


    # timer callback function 
    def callback_showTime(self):
        # showing text 
        self.label.setText(self.gettimertext())

    def httpGetReqToURL(self, url):
        resp = requests.get(url)
        data = json.loads(resp.text)
        return data

    # http request
    def httpPostReqToURL(self, url, data):
        res = requests.post(url,
                            json.dumps(data),
                            headers={'Content-Type': 'application/json'}
                            )
        return res





    # init button
    def Init(self):
        url = JUDGESERVER_REQUEST_URL
        req_data = {"change_state": "init"}
        res = self.httpPostReqToURL(url, req_data)
        return res

    # start button
    def Start(self):
        url = JUDGESERVER_REQUEST_URL
        req_data = {"change_state": "start"}
        res = self.httpPostReqToURL(url, req_data)
        return res

    # stop button
    def Stop(self):
        url = JUDGESERVER_REQUEST_URL
        req_data = {"change_state": "stop"}
        res = self.httpPostReqToURL(url, req_data)
        return res

    # lap count button
    def LapCount_plus(self):
        # request POST data to server
        url = JUDGESERVER_UPDATEDATA_URL
        req_data = {"lap_count": 1}
        res = self.httpPostReqToURL(url, req_data)
        return res

    def LapCount_minus(self):
        # request POST data to server
        url = JUDGESERVER_UPDATEDATA_URL
        req_data = {"lap_count": -1}
        res = self.httpPostReqToURL(url, req_data)
        return res

    # courseout count button
    def CourseOutCount_plus(self):
        # request POST data to server
        url = JUDGESERVER_UPDATEDATA_URL
        req_data = {"courseout_count": 1}
        res = self.httpPostReqToURL(url, req_data)
        return res

    def CourseOutCount_minus(self):
        # request POST data to server
        url = JUDGESERVER_UPDATEDATA_URL
        req_data = {"courseout_count": -1}
        res = self.httpPostReqToURL(url, req_data)
        return res

    def gettimertext(self):
        # request GET data to server
        url = JUDGESERVER_GETSTATE_URL
        data = self.httpGetReqToURL(url)
        time = data["judge_info"]["time"]
        lap_count = data["judge_info"]["lap_count"]
        courseout_count = data["judge_info"]["courseout_count"]
        #courseout_count = 0
        judgestate = data["judge_info"]["judgestate"]

        # timer text
        passed_time_str = str('{:.2f}'.format(time))
        lap_count_str = str(lap_count)
        courseout_count_str = str(courseout_count)
        judgestate_str = str(judgestate)

        text = "JudgeState: " + judgestate_str + "\n" \
               + "Time: " + passed_time_str + " (s)" + "\n" \
               + "LAP: " + lap_count_str + "  " \
               + "CourseOut: " + courseout_count_str

        return text

# create pyqt5 app 
App = QApplication(sys.argv) 
  
# create the instance of our Window 
window = Window() 
  
# start the app 
sys.exit(App.exec()) 
