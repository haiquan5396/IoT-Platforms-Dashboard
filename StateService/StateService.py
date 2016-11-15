from flask import Flask, render_template, jsonify, request
from threading import Timer, Thread
from platform_driver import openhab, home_assistant
from influxdb import InfluxDBClient
import datetime

app = Flask(__name__)
@app.route("/")
def hello_world():
    return "hello_world"


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

def update_openhab_state():
    oh = openhab.openhab_driver()
    if oh.check_status() == True:
        items = oh.get_all_sensor_informations()
        print items
        global client
        for item in items:
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

def update_homeassistant_state():
    ha = home_assistant.home_assistant_driver()
    print "1"
    if ha.check_status() == True:
        print "2"
        items = ha.get_all_sensor_informations()
        print items
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

def update_sensor_state():
    # update_openhab_state();
    update_homeassistant_state()
if __name__ == "__main__":
    client = influxdb_init()
    scheduler = Scheduler(3 , update_sensor_state)
    scheduler.start()
    app.run(host='0.0.0.0', port=1337)
    scheduler.stop()