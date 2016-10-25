####regular method call to openhabAPI
class openhab_driver:
    host = None
    port = None
    def __init__(self, host=None, port=None):
        self.host = host if host is not None else "localhost"
        self.port = port if port is not None else "8080"

##  get infomation from API
    #get name
    def get_all_sensor_names(self):
        pass

    #get name and state
    def get_all_sensor_states(self):
        pass

    #get name,state
    def get_sensor_infomations_by_type(self, type):
        pass

    #get name,state and type
    def get_all_sensor_informations(self):
        pass

    #get sensor state by name
    def get_sensor_state(self, name):
        pass

    #get sensor type  by name
    def get_sensor_type(self, name):
        pass

##  set sensor state

    # set sensor state by name
    def set_sensor_state(self, name):
        pass

    # set sensors state by type
    def set_sensors_state_by_type(self, type, state):
        pass

    #switch state of switch, light, door,...
    def switch_sensors_state(self, type, state):
        pass