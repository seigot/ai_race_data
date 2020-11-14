# -*- coding: utf-8 -*-

import requests
from time import sleep
import json
import numpy as np
import cv2
import os
import copy
import datetime

class StatusWindow:
    def __init__(self, w_name=None, window_size=(960,1280), object_info_path=None, picture_path=None ):
        test=0
        print(self.startrace())
        sleep(1)
        print(self.urlreq())
        print(self.sendToJudge())
        print(self.sendCnt())

    def startrace(self):
        self.player_name = "hoge"
        self.side = "r"
        target_id = 1
        test_state = "test"
        self.judge_url="http://127.0.0.1:5000/raceState/start"
        
        data = {}
        res = requests.post(self.judge_url,
                            json.dumps(data),
                            headers={'Content-Type': 'application/json'}
                            )
        return res

    def urlreq(self):
        resp = requests.get("http://127.0.0.1:5000/raceState")
        data = json.loads(resp.text)
        time = data["judge_info"]["time"]
        lap_count = data["judge_info"]["lap_count"]
        #print(str(time) + " " + str(lap))
        print(str('{:.2f}'.format(time)) + " " + str(lap_count))

        return resp.text


    def sendToJudge(self):
        self.player_name = "hoge"
        self.side = "r"
        target_id = 1
        test_state = "test"
        self.judge_url="http://127.0.0.1:5000/raceState/state"
        
        data = {"name": self.player_name, "side": self.side, "id": target_id, "state": test_state}
        res = requests.post(self.judge_url,
                            json.dumps(data),
                            headers={'Content-Type': 'application/json'}
                            )

        return res

    def sendCnt(self):
        data = {"cnt": 1}
        self.judge_url="http://localhost:5000/raceState/update"
        res = requests.post(self.judge_url,
                            json.dumps(data),
                            headers={'Content-Type': 'application/json'}
                            )

        return res

if __name__ == "__main__":
    sw = StatusWindow(w_name="Onigiri War")
    
    #display = sw.initWindow()
#
 #   while(True):
  #      sw.update(display)
   #     sleep(1)
