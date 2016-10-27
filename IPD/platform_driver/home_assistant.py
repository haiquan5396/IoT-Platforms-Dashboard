import requests
import json
class home_assistant:
    host = None
    port = None
    def __init__(self, host=None, port=None):
        self.host = host if host is not None else "localhost"
        self.port = port if port is not None else "8123"

        self.url = "http://" + self.host + ":" + self.port
        try:
            connect = requests.get(self.url + "/api")
            response_text = json.loads(connect.content)
            if (connect.status_code == 200) and (response_text['message'] == "API running."):
                print "[SUCCESS] Connected to Home-Assistant"
            else:
                print "[!!!ERROR] Wrong host or port"
                raise Exception()
        except Exception:
            print "Unable to connect to Home Assistant"

    def get_states_json(self):
        response = requests.get(self.url + "/api/states")
        return json.loads(response.content)


    def get_state_json_by_entityid(self, entityid):
        try:
            response = requests.get(self.url + "/api/states/" + entityid)
            if response.status_code != 200:
                raise Exception()
            else:
                return json.loads(response.content)
        except Exception:
            print "[ERROR] Invalid entity_id: " + entityid
        return None

##  get infomation from API
    #get entity_id (~~type.name)
    def get_all_sensor_entityid(self):
        entity_ids = []
        data = self.get_states_json()
        for item in data:
            entity_ids.append(item["entity_id"])
        return entity_ids

    #get entity_id and state
    def get_all_sensor_states(self):
        states = []
        data = self.get_states_json()
        for item in data:
            state = []
            state.append(item["entity_id"])
            state.append(item["state"])
            states.append(state)
        return states

    #get entity_id, state { [id, state], []........}
    def get_sensor_infomations_by_type(self, type="all"):
        #if type is not given then return state of all sensors
        if type == "all":
            return self.get_all_sensor_states()

        states = []
        data = self.get_states_json()
        for item in data:
            entity_id = item["entity_id"]
            if type == entity_id.split(".")[0]:
                state = []
                state.append(entity_id)
                state.append(item["state"])
                states.append(state)
        return states

    #get entity_id, state, type {[id, state, type], []....}
    def get_all_sensor_informations(self):
        states = []
        data = self.get_states_json()
        for item in data:
            entity_id = item["entity_id"]
            type = entity_id.split(".")[0]
            state = []
            state.append(entity_id)
            state.append(item["state"])
            state.append(type)
            states.append(state)
        return states


    #get sensor state by entity_id
    def get_sensor_state(self, entity_id):
        data = self.get_state_json_by_entityid(entity_id)
        if data == None:
            print "No entityid match"
            return
        else:
            return data["state"]

    #get sensor type  by entity_id
    def get_sensor_type(self, entity_id):
        data = self.get_state_json_by_entityid(entity_id)
        if data == None:
            print "No entityid match"
            return
        else:
            return entity_id.split(".")[0]

##  set sensor state
    # set sensor state by entity_id
    def set_sensor_state(self, entity_id, state):
        url = self.url + "/api/states/" + entity_id
        payload = {'state':state}
        headers = {'Content-Type': 'application/json'}

        r = requests.post(url, data = json.dumps(payload), headers= headers)

        if r.status_code == 200:
            return "SUCCESS"
        else:
            return "ERROR"


    #
    # # set sensors state by type
    # def set_sensors_state_by_type(self, type, state):
    #     pass
    #
    # # switch state of switch, light, door,...
    # def switch_sensors_state(self, type, state):
    #     pass