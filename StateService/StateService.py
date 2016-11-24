from flask import Flask, jsonify, request, abort
from threading import Timer, Thread
from platform_driver import openhab, home_assistant
from influxdb import InfluxDBClient
from time import sleep
import json


app = Flask(__name__)

def influxdb_init():
    host='localhost'
    # host = os.environ['INFLUX_HOST']  # influxdb host name
    port = 8086
    user = 'root'
    password = 'root'
    dbname = 'ipd'
    dbuser = ''
    dbuser_password = ''
    client = InfluxDBClient(host, port, user, password, dbname)
    client.drop_database(dbname)  # 2.10 delete_database / 2.12: drop_database
    client.create_database(dbname)
    return client

client = influxdb_init()

#================================================================================================================#

@app.route("/")
def hello_world():
    return "hello_world"

#get all sensor state via driver
@app.route("/api/states", methods=["GET"])
def get_sensor_states():
    oh = openhab.openhab_driver()
    ha = home_assistant.home_assistant_driver()
    items = []
    oh_items = []
    ha_items = []
    if oh.check_status() == True:
        oh_items = oh.get_all_sensor_informations()
    if ha.check_status() == True:
        ha_items = ha.get_all_sensor_informations()

    items = oh_items + ha_items
    return json.dumps(items)

@app.route("/api/states/<name>",methods=["GET"])
def get_sensor_state_by_name(name):
    global client
    print "get state of " + name
    # todo: check sensor valid or not
    result_set = client.query('SELECT * FROM \"' + name + '\" ORDER BY time DESC LIMIT 1')
    return json.dumps(list(result_set)[0][0]) ##{"platform": "openhab", "state": "ON", ....}

@app.route("/api/states/history/<name>", methods=["GET"])
def get_state_history_by_name(name):
    global client
    print "get history of" + name
    # todo: check sensor valid or not
    result_set = client.query('SELECT * FROM \"' + name + '\" ORDER BY time DESC LIMIT 5')
    return json.dumps(list(result_set)[0])

@app.route("/api/states/<name>", methods=["POST"])
def set_sensor_state_by_name(name):
    if not request.json or not 'state' in request.json:
        abort(400)
    state = request.json['state']
    global client
    print "set state of "+name
    #todo: check sensor valid or not
    result_set = client.query('SHOW TAG VALUES FROM \"'+ name + '\" WITH KEY = "platform"')
    platform = list(result_set)[0][0]["platform"]
    if platform == "openhab":
        oh = openhab.openhab_driver()
        result = oh.set_sensor_state(name,state)
        if result == "SUCCESS":
            print "SUCCESS"
        else:
            print "ERROR"
    elif platform == "home_assistant" :
        ha = home_assistant.home_assistant_driver()
        result = ha.set_sensor_state(name,state)
        if result == "SUCCESS":
            print "SUCCESS"
        else:
            print "ERROR"
    return jsonify(request.json) , 201

@app.route("/api/states/type/<type>", methods=["POST"])
def set_sensor_state_by_type(type):
    if not request.json or not 'state' in request.json:
        abort(400)
    state = request.json['state']
    oh = openhab.openhab_driver()
    ha = home_assistant.home_assistant_driver()

    if type == "Lights":
        items = []
        items.extend(oh.get_sensor_infomations_by_type("Lights"))
        items.extend(ha.get_sensor_infomations_by_type("light"))

        for item in items:
            set_sensor_state_by_name(item[0])
        return jsonify(json.dumps(items))
    else:
        return jsonify({"status":"fail"}) , 201

#=================================================================================================================#
class Scheduler(object):
    def __init__(self, sleep_time, function):
        self.sleep_time = sleep_time
        self.function = function
        self._t = None

    def start(self):
        if self._t is None:
            self._t = Timer(self.sleep_time, self._run)
            self._t.start()
        else:
            raise Exception("this timer is already running")

    def _run(self):
        self.function()
        self._t = Timer(self.sleep_time, self._run)
        self._t.start()

    def stop(self):
        if self._t is not None:
            self._t.cancel()
            self._t = None


def update_openhab_state(influxdb_client):
    client = influxdb_client
    oh = openhab.openhab_driver()
    if oh.check_status() == True:
        items = oh.get_all_sensor_informations()
        # print items

        for item in items:
            # sleep(0.1)
            # start_time = time.time()
            # print "a"
            # print("--- %s seconds ---" % (time.time() - start_time))
            json_body = [
                {
                    "measurement": item[0],
                    "tags": {
                        "platform": "openhab"
                        },
                    "fields": {
                        "soft_name": item[0],
                        "state": item[1],
                        "type": item[2],
                    }
                }
            ]
            client.write_points(json_body)
            # sleep(0.05)

    else:
        print "[!ERROR] openhab is not running in your port"

def update_homeassistant_state(influxdb_client):
    client = influxdb_client
    ha = home_assistant.home_assistant_driver()
    if ha.check_status() == True:
        print "2"
        items = ha.get_all_sensor_informations()
        # print items
        for item in items:
            soft_name = item[0].split(".")[1]
            json_body = [
                {
                    "measurement": item[0],
                    "tags": {
                        "platform": "home_assistant"
                    },
                    "fields": {
                        "soft_name": soft_name,
                        "state": item[1],
                        "type": item[2],
                    }
                }
            ]
            client.write_points(json_body)
            # sleep(0.05)
    else:
        print "[!ERROR] Home-assistant is not running in your port"
def update_sensor_state():
    global client
    update_openhab_state(client)
    update_homeassistant_state(client)
    # oh = openhab.openhab_driver()
    # print home_assistant.home_assistant_driver().get_sensor_infomations_by_type("switch")
    # print oh.get_sensor_infomations_by_type("Lights")

def pass_method():
    pass
if __name__ == "__main__":
    scheduler = Scheduler(1 , update_sensor_state)
    scheduler.start()
    app.run(host='0.0.0.0', port=1337)
    scheduler.stop()