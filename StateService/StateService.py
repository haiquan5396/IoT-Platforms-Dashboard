from flask import Flask, jsonify, request, abort
from platform_driver.driver_client import Drive_client
from influxdb import InfluxDBClient
import json
from scheduler import Scheduler
from influxdb_data_recorder import Data_recorder
#============ import for cross origin
from flask import make_response, current_app
from datetime import timedelta
from functools import update_wrapper

#=============================================================
def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator
#===================================================================   
app = Flask(__name__)

# @app.after_request

# def after_request(response):
#   response.headers.add('Access-Control-Allow-Origin', '*')
#   response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#   response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
#   return response


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
@crossdomain(origin="*")
def hello_world():
    return "hello_world"

@app.route("/api/states", methods=["GET"])
@crossdomain(origin="*")
def get_sensor_states():
    items = []
    for platform in list_platforms:
        items.extend(platform.driver.get_all_sensors_infomation())
    # print items
    return json.dumps(items)

@app.route("/api/states/<name>",methods=["GET"])
@crossdomain(origin="*")
def get_sensor_state_by_name(name):
    global db_client
    print "get state of " + name
    # todo: check sensor valid or not
    result_set = db_client.query('SELECT * FROM \"' + name + '\" ORDER BY time DESC LIMIT 1')
    print json.dumps(list(result_set)[0][0])
    return json.dumps(list(result_set)[0][0])  ##{"platform": "openhab", "state": "ON", ....}

@app.route("/api/states/history/<name>/<select_type>/<time_start>", methods=["GET"])
@crossdomain(origin="*")
def get_state_history_by_name(name, select_type,time_start):
    global db_client
    print "get history of" + name
    if select_type == "first_time":
        # time_start o day la khoang thoi gian can truy van < Vi du: 5phut, 20phut, 30phut
        result_set = db_client.query('SELECT * FROM \"' + name + '\" WHERE time >= now() - ' + time_start +'m')
        return json.dumps(list(result_set)[0])
    else:
        # time_start o day la moc  thoi gian
        result_set = db_client.query('SELECT * FROM \"' + name + '\" WHERE time >= \''+ time_start + '\'')
        return json.dumps(list(result_set)[0])

@app.route("/api/states/<name>", methods=["POST","OPTIONS"])
@crossdomain(origin="*",headers=['origin', 'content-type', 'accept'])
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

@app.route("/api/states/type/<type>", methods=["POST","OPTIONS"])
@crossdomain(origin="*")
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
    app.run(host='0.0.0.0', port=1337, threaded=True)
    scheduler.stop()