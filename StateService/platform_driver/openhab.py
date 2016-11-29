import requests
import xml.etree.ElementTree as ET
from driver_base import Driver_base

class openhab_driver(Driver_base):
    def __init__(self, host=None, port=None):
        # super.__init__(self)
        self.host = host if host is not None else "localhost"
        self.port = port if port is not None else "8080"
        self.url = "http://" + self.host + ":" + self.port

        if self.check_status() == True:
            print "OpenHab is running, Connected"
        else:
            print "Unable to connect to OpenHabAPI, Wrong host or port"

    ############ Get states from Platform api (json or xml..)
    #------get states tree
    def get_states_resource(self):
        if self.check_status() == True:
            response = requests.get(self.url+"/rest/items")
            root = ET.fromstring(response.content)
            return root
        else:
            return None

    def get_state_resource_by_name(self, name):
        response = requests.get(self.url + "/rest/items/" + name)
        if response.status_code != 200: ## That means wrong port or name
            return None ## nothing to return here
        else:
            root = ET.fromstring(response.content)
            return root

    #############
    #------- get all infomation ( name/id, state, itemtype )
    def get_all_sensors_infomation(self):
        states = []
        root = self.get_states_resource()

        if root == None: ## if root == None mean server deaded or sth like that
            print "Your server is not running probably"
            return None

        for item in root.findall("item"):
            if item.find("type").text == "GroupItem":
                continue
            state = []
            state.append(item.find("name").text)
            state.append(item.find("state").text)
            state.append(item.find("type").text)
            states.append(state)
        return states

    #------- get all infomation by type ( name/id , state )
    def get_all_sensors_infomation_by_type(self, type):
        if type.lower() == "lights" or type.lower() == "light":
            type = "Lights"
        else:
            print "only support light type"
            return []

        # return name and state {[name,state],[..]}
        states = []
        root = self.get_state_resource_by_name(type)
        if root == None:
            print "No group has name '\Lights\'"
            return []
        for member in root.findall("members"):
            state = []
            state.append(member.find("name").text)
            state.append(member.find("state").text)
            states.append(state)
        return states


    #------- get sensor state by name
    def get_sensor_state(self, name):
        root = self.get_state_resource_by_name(name)
        if root == None:
            print "No sensor name match"
            return
        else:
            return root.find("state").text

    #------- set sensor state
    def set_sensor_state(self, name, state):
        if requests.put(self.url + "/rest/items/" + name + "/state", state).status_code == 200:
            return "SUCCESS"
        return "ERROR"