import requests
import json
from driver_base import Driver_base
class home_assitant(Driver_base):
    host = None
    port = None
    url = None

    def __init__(self, host=None, port=None):
        # super.__init__(self)
        self.host = host if host is not None else "localhost"
        self.port = port if port is not None else "8123"
        self.url = "http://" + self.host + ":" + self.port

        if self.check_status() == True:
            print "Home-assistant is running, Connected"
        else:
            print "Unable to connect to HomeAsisstantAPI, Wrong host or port"

    def check_status(self):
        connect = requests.get(self.url)
        if connect.status_code == 200:
            return True
        else:
            return False

    ############ Get states from Platform api (json or xml..)
    def get_states_resource(self):
        if self.check_status() == True:
            response = requests.get(self.url + "/api/states")
            return json.loads(response.content)
        else:
            return None

    def get_state_resource_by_name(self, entityid):
        response = requests.get(self.url + "/api/states/" + entityid)
        if response.status_code != 200:
            return None
        else:
            return json.loads(response.content)

    #############
    #------- get all infomation ( name/id, state, itemtype )
    def get_all_sensors_infomation(self):
        states = []
        data = self.get_states_resource()
        if data == None:
            print "Your HA server is not running probably"
            return None

        for item in data:
            entity_id = item["entity_id"]
            type = entity_id.split(".")[0]
            if type == "group":
                continue
            state = []
            state.append(entity_id)
            state.append(item["state"])
            state.append(type)
            states.append(state)
        return states
    #------- get all infomation by type ( name/id , state )
    def get_all_sensors_infomation_by_type(self, type):
        if type.lower() == "lights" or type.lower() == "light":
            type = "light"
        else:
            print "only support light type"
            return []

        states = []
        data = self.get_states_resource()
        for item in data:
            entity_id = item["entity_id"]
            if type == entity_id.split(".")[0]:
                state = []
                state.append(entity_id)
                state.append(item["state"])
                states.append(state)
        return states


    #------- get sensor state by name
    def get_sensor_state(self, entity_id):
        data = self.get_state_resource_by_name(entity_id)
        if data == None:
            print "No entityid match"
            return None
        else:
            return data["state"]

    #------- set sensor state
    def set_sensor_state(self, entity_id, state):
        url = self.url + "/api/states/" + entity_id
        payload = {'state':state}
        headers = {'Content-Type': 'application/json'}

        r = requests.post(url, data = json.dumps(payload), headers= headers)

        if r.status_code == 200:
            return "SUCCESS"
        else:
            return "ERROR"
