from flask import Flask, render_template, jsonify, request
from threading import Timer, Thread
from platform_driver import openhab, home_assistant
from influxdb import InfluxDBClient
import json
from time import sleep
import time

app = Flask(__name__)
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

@app.route("/   api/state/<string:name>",methods=["GET"])
def get_sensor_state_by_name(name):
    result = client.query('select * from '+name)
    return result

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
    return client

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
    else:
        print "[!ERROR] Home-assistant is not running in your port"
def update_sensor_state():
    client = influxdb_init()
    update_openhab_state(client)
    update_homeassistant_state(client)

def pass_method():
    pass
if __name__ == "__main__":

    scheduler = Scheduler(3 , update_sensor_state)
    # scheduler = Scheduler(3, pass_method)
    scheduler.start()
    app.run(host='0.0.0.0', port=1337)
    scheduler.stop()