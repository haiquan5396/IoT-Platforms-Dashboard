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

##  get infomation from API
    #get entity_id (~~type.name)
    def get_all_sensor_entity(self):
        pass

    #get entity_id and state
    def get_all_sensor_states(self):
        pass

    #get entity_id, state
    def get_sensor_infomations_by_type(self, type):
        pass

    #get entity_id, state, type
    def get_all_sensor_informations(self):
        pass

    #get sensor state by entity_id
    def get_sensor_state(self, entity_id):
        pass

    #get sensor type  by entity_id
    def get_sensor_type(self, entity_id):
        pass

##  set sensor state
    # set sensor state by entity_id
    def set_sensor_state(self, entity_id):
        pass

    # set sensors state by type
    def set_sensors_state_by_type(self, type, state):
        pass

    # switch state of switch, light, door,...
    def switch_sensors_state(self, type, state):
        pass