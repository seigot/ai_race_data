# -*- coding: utf-8 -*-
import os
import datetime
import time
import argparse
## flask
from flask import Flask, request, jsonify, render_template
from flask import send_from_directory
## for server debug logger
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)


#class Target:
#    ## [future work] Set, if any Obstacle or Other item state is necessary...
#    def __init__(self, name, id, point):
#        self.id = id
#        self.name = name
#        self.player = "n"
#        self.point = point
#
#    def makeJson(self):
#        json = {
#            "name": self.name,
#            "player": self.player,
#            "point": self.point,
#        }
#        return json

#class Response:
#    def __init__(self):
#        self.mutch = False
#        self.new = False
#        self.error = "yet init"
#        self.target = None
#
#    def makeJson(self):
#        if self.target is None:
#            target = None
#        else:
#            target = self.target.makeJson()
#        json = {
#            "mutch": self.mutch,
#            "new": self.new,
#            "error": self.error,
#            "target": target
#        }
#        return json


class JUDGE:
    def __init__(self, matchtime, extendtime):
        #self.RaceStateClass = RaceState(matchtime, extendtime)

        self.initializeTimer()
        self.matchtime = matchtime # [sec]
        #self.state = "end"
        self.lap_count = 0

    def initializeTimer(self):
        self.init_time = None
        self.start_time = 0.00
        self.passed_time = 0.00
        self.stoped_time = 0.00

    def getRaceStateJson(self):
        is_finished = self.updateTime()
        if is_finished:
            self.writeResult()
        return self.makeJson()

    def startRace(self):
        print("start startRace()")
        self.start_time = time.time()
        ret = "ok"
        return ret

    def updateRace(self, body):
        print("start updateRace()")
        print(body)
        if "cnt" in body:
            print("OKOKOKOK")
        
        cnt = body["cnt"]
        print(cnt)
        self.lap_count = self.lap_count + 1
        ret = "ok"
        return ret

    def updateTime(self):
        app.logger.info("updateTime")
        if self.start_time == 0.00:
            self.passed_time = 0.00
            return False

        self.passed_time = time.time() - self.start_time
        print(self.passed_time)

        app.logger.info("passed_Time {}".format(self.passed_time))
        return False

    def makeJson(self):
        json = {
            "field_info": {
                "state": "None",
            },
            "car_info": {
                "state": "None",
            },
            "judge_info": {
                "time": self.passed_time,
                "lap_count": self.lap_count,
            },
            "debug_info": {
                "state": "None",
            },
        }
        return json

    def makeCsv(self):
        '''
        for debug, convert race_state to string
        '''
        csv_list = ["{0:%y%m%d-%H%M%S}".format(datetime.datetime.now()),
                    str(self.players["r"]),
                    str(self.players["b"]),
                    str(self.scores["r"]),
                    str(self.scores["b"]),
                    str(self.state),
                    str(self.stoped_time),
                    ' '.join([str(t.makeJson()) for t in self.targets]),
                    ]
        csv = ','.join(csv_list)
        return csv

    def setStateStop(self):
        self.state = "stop"
        self.initializeTimer()

    def judgeTargetId(self, player_name, player_side, target_id):
        '''
        target_id must be string and length is "4"
        return "False" or "target json"
        '''
        # make Response object
        response = Response()

        # Update time and check match time
        is_finished = self.updateTime()
        if is_finished:
            self.writeResult()

        # check state is running
        if self.RaceStateClass.state != "running":
            response.error = "ERR state is not running"
            return response.makeJson()

        for target in self.targets:
            if target_id == target.id:
                is_new = self.updateRaceState(target, player_name, player_side)
                response.mutch = True
                response.new = is_new
                response.error = "no error"
                response.target = target

                return response.makeJson()
        response.error = "ERR not mutch id"
        return response.makeJson()


    def updateRaceState(self, target, player_name, player_side):
        # new target or not
        if not target.player == "n":
            is_new =  False
        else:
            is_new = True

        # change target player
        target.player = player_side

        # recount score
        red = 0
        blue = 0
        for target_ in self.targets:
            if target_.player == 'n':
                pass
            elif target_.player == 'b':
                blue += int(target_.point)
            elif target_.player == 'r':
                red += int(target_.point)
            else:
                app.logger.error("ERROR recount score")
        self.scores['b'] = blue
        self.scores['r'] = red

        return is_new 

    def registPlayer(self, name):
        if self.players['r'] == "NoPlayer":
            self.players['r'] = name
            ret = {"side": "r", "name": name}
        elif self.players['b'] == "NoPlayer":
            self.players['b'] = name
            ret = {"side": "b", "name": name}
        else:
            ret = "##Errer 2 player already registed"
        return ret

    def registTarget(self, name, target_id, point):
        target = Target(name, target_id, point)
        self.targets.append(target)
        return target.name

    def setState(self, state):
        app.logger.info("setState")
        if state == "end":
            self.state = state
        elif state == "running":
            pass

        return state

    def writeResult(self):
        ## For Debug, output Result file.
        result_string = self.makeCsv()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        log_file_path = script_dir + "/log/" + "game_result.log"
        with open(log_file_path, "a") as f:
            f.write(result_string + "\n")
        app.logger.info("Write Result {}".format(result_string))

### API definition
@app.route('/')
def index():
    ip = request.remote_addr
    app.logger.info("GET /(root) "+ str(ip))
    return render_template('index.html')

#@app.route('/favicon.ico')
#def favicon():
#    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='static/')

@app.route('/raceState/start', methods=['POST'])
def startRace():
    print("request to POST /raceState/start")
    body = request.json
    ip = request.remote_addr
    app.logger.info("POST /raceState/start " + str(ip) + str(body))
    response = judge.startRace()
    res = response
    app.logger.info("RESPONSE /raceState/start " + str(ip) + str(res))
    return jsonify(res)

@app.route('/raceState/update', methods=['POST'])
def updateRace():
    print("request to POST /raceState/update")
    body = request.json
    ip = request.remote_addr
    app.logger.info("POST /raceState/update " + str(ip) + str(body))
    response = judge.updateRace(body)
    res = response
    app.logger.info("RESPONSE /raceState/update " + str(ip) + str(res))
    return jsonify(res)

#@app.route('/submits', methods=['POST'])
#def judgeTargetId():
#    print("request to POST /submits")
#    body = request.json
#    ip = request.remote_addr
#    app.logger.info("POST /submits " + str(ip) + str(body))
#    player_name = body["name"]
#    player_side = body["side"]
#    target_id = body["id"]
#    response = judge.judgeTargetId(player_name, player_side, target_id)
#    res = response
#    app.logger.info("RESPONSE /submits " + str(ip) + str(res))
#    return jsonify(res)


@app.route('/raceState', methods=['GET'])
def getState():
    print("request to GET /raceState")
    ip = request.remote_addr
    #app.logger.info("GET /raceState " + str(ip))
    state_json = judge.getRaceStateJson()
    res = state_json
    #app.logger.info("RESPONSE /raceState "+ str(ip) + str(res))
    return jsonify(res)


#@app.route('/raceState/players', methods=['POST'])
#def registPlayer():
#    print("request to GET /raceState/players")
#    body = request.json
#    ip = request.remote_addr
#    app.logger.info("POST /raceState/players " + str(ip) + str(body))
#    name = body["name"]
#    ret = judge.registPlayer(name)
#    res = ret
#    app.logger.info("RESPONSE /raceState/players " + str(ip)+ str(res))
#    return jsonify(res)


#@app.route('/raceState/targets', methods=['POST'])
#def registTarget():
#    print("request to POST /raceState/targets")
#    body = request.json
#    ip = request.remote_addr
#    app.logger.info("POST /raceState/targets " + str(ip)+ str(body))
#    name = body["name"]
#    target_id = body["id"]
#    print(str(name) + " " + str(target_id))
#    #point = body["point"]
#    #ret = judge.registTarget(name, target_id, point)
#    ret = "test"
#    res = {"name": ret}
#    app.logger.info("RESPONSE /raceState/targets " + str(ip)+ str(res))
#    return jsonify(res)

@app.route('/raceState/state', methods=['POST'])
def setState():
    print("request to POST /raceState/state")
    body = request.json
    ip = request.remote_addr
    app.logger.info("POST /raceState/state " + str(ip)+ str(body))
    state = body["state"]
    print(state)
    ret = judge.setState(state)
    res =  {"state": ret}
    app.logger.info("RESPONSE /raceState/state " + str(ip)+ str(res))
    return jsonify(res)


#@app.route('/reset', methods=['GET'])
#def reset():
#    print("request to GET /reset")
#    ip = request.remote_addr
#    app.logger.info("GET /reset " + str(ip))
#    global judge
#    judge = JUDGE(args.matchtime, args.extendtime)
#    res = "reset"
#    app.logger.info("RESPONSE /reset " + str(ip) + str(res) + str(args.matchtime) + str(args.extendtime))
#    return jsonify(res)


#@app.route('/test', methods=['GET'])
#def getTest():
#    print("request to GET /test")
#    ip = request.remote_addr
#    app.logger.info("GET /test "+ str(ip))
#    res = { "foo": "bar", "hoge": "hogehoge" }
#    app.logger.info("RESPONSE /test "+ str(ip) + str(res))
#    return jsonify(res)


if __name__ == '__main__':
    # argument parse
    parser = argparse.ArgumentParser(description='burger_war judger server')
    parser.add_argument('--matchtime', '--mt', default=float('inf'), type=float, help='match time [sec]')
    parser.add_argument('--extendtime','--et', default=60, type=float, help='extend time [sec]')
    args = parser.parse_args()

    # global object judge
    judge = JUDGE(args.matchtime, args.extendtime)

    # app for debug
    now = datetime.datetime.now()
    now_str = now.strftime("%y%m%d_%H%M%S")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_file_path = script_dir + "/log/" + now_str + ".log"
    handler = RotatingFileHandler(log_file_path, maxBytes = 1000000, backupCount=100)
    handler.setLevel(logging.INFO)
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True, host='0.0.0.0', port=5000)
