import requests
class Base(object):
    host = None
    port = None
    url = None

    def __init__(self, host=None, port=None):
        pass

    def check_status(self):
        connect = requests.get(self.url)
        if connect.status_code == 200:
            return True
        else:
            return False

    ############ Get states from Platform api (json or xml..)
    def get_states_resource(self):
        pass

    def get_state_resource_by_name(self):
        pass

    #############
    #------- get all infomation ( name/id, state, itemtype )
    def get_all_sensors_infomation(self):
        pass
    #------- get all infomation by type ( name/id , state )
    def get_all_sensors_infomation_by_type(self):
        pass

    #------- get sensor state by name
    def get_sensor_state(self, name):
        pass

    #------- set sensor state
    def set_sensor_state(self, name, state):
        pass
