from flask import Flask, jsonify, request, abort
from platform_driver.driver_client import Drive_client
from influxdb import InfluxDBClient
import json
from scheduler import Scheduler
from influxdb_data_recorder import Data_recorder

app = Flask(__name__)

def platform_init():
    list = []
    platforms_name = ["openhab","home-assistant"]
    for name in platforms_name:
        list.insert(0,Drive_client(name))
    return list

list_platforms = platform_init()
data_recoder = Data_recorder(list_platforms)
db_client = data_recoder.db_client

@app.route("/")
def hello_world():
    return "hello_world"

@app.route("/api/states", methods=["GET"])
def get_sensor_states():
    items = []
    for platform in list_platforms:
        items.extend(platform.driver.get_all_sensors_infomation())
    print items
    return json.dumps(items)

@app.route("/api/states/<name>",methods=["GET"])
def get_sensor_state_by_name(name):
    global db_client
    print "get state of " + name
    # todo: check sensor valid or not
    result_set = db_client.query('SELECT * FROM \"' + name + '\" ORDER BY time DESC LIMIT 1')
    return json.dumps(list(result_set)[0][0])  ##{"platform": "openhab", "state": "ON", ....}

@app.route("/api/states/history/<name>", methods=["GET"])
def get_state_history_by_name(name):
    global db_client
    print "get history of" + name
    # todo: check sensor valid or not
    result_set = db_client.query('SELECT * FROM \"' + name + '\" ORDER BY time DESC LIMIT 5')
    return json.dumps(list(result_set)[0])

@app.route("/api/states/<name>", methods=["POST"])
def set_sensor_state_by_name(name):
    if not request.json or not 'state' in request.json:
        abort(400)
    state = request.json['state']
    global db_client
    print "set state of " + name

    result_set = db_client.query('SHOW TAG VALUES FROM \"' + name + '\" WITH KEY = "platform"')
    platform_name = list(result_set)[0][0]["platform"]

    for platform in list_platforms:
        if platform.platform == platform_name:
            result = platform.driver.set_sensor_state(name,state)
            if result == "SUCCESS":
                print "SUCCESS"
            else:
                print "ERROR"
    return jsonify(request.json), 201

@app.route("/api/states/type/<type>", methods=["POST"])
def set_sensor_state_by_type(type):
    if not request.json or not 'state' in request.json:
        abort(400)
    state = request.json['state']
    items = []
    if type == "Lights":
        for platform in list_platforms:
            items.extend(platform.driver.get_all_sensors_infomation_by_type("Light"))
        for item in items:
            set_sensor_state_by_name(item[0])
        return jsonify(json.dumps(items))
    else:
        return jsonify({"status":"type are not support"}), 201

#===================================================================
def pass_method():
    pass
if __name__ == "__main__":
    scheduler = Scheduler(1, data_recoder.update_data)
    scheduler.start()
    app.run(host='0.0.0.0', port=1337)
    scheduler.stop()