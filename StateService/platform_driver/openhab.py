import requests
import xml.etree.ElementTree as ET

####regular method call to openhabAPI
class openhab_driver:
    host = None
    port = None
    url = None
    def __init__(self, host=None, port=None):
        self.host = host if host is not None else "localhost"
        self.port = port if port is not None else "8080"
        self.url = "http://" + self.host + ":" + self.port
        try:
            connect = requests.get(self.url)
            print connect.status_code
            if connect.status_code == 200:
                print "[SUCCESS] Connected to OpenHab"
            else:
                print "[!!!ERROR] Wrong host or port"
                raise  Exception()
                return None
        except Exception:
            print "Unable to connect to OpenHabAPI"
## check status of server
    def check_status(self):
        connect = requests.get(self.url)
        if connect.status_code == 200:
            return True
        else:
            return False


##  get XML from API and parse to XML-Tree return root
    def get_states_tree(self):
        response = requests.get(self.url+"/rest/items")
        root = ET.fromstring(response.content)
        return root

    def get_state_tree_by_name(self, name):
        try:
            response = requests.get(self.url + "/rest/items/"+ name)
            if response.status_code != 200:
                raise Exception()
            else:
                root = ET.fromstring(response.content)
                return root
        except Exception:
            print "[!!!ERROR] Invalid sensor name : " + name
        return None

##  get infomation from API
    #get name
    def get_all_sensor_names(self):
        names = []
        root = self.get_states_tree()
        for item in root.findall("item"):
            names.append(item.find("name").text)
        return names

    #get name and state
    def get_all_sensor_states(self):
        #return name and state {[name,state],[..]}
        states = []
        root = self.get_states_tree()
        for item in root.findall("item"):
            state = []
            state.append(item.find("name").text)
            state.append(item.find("state").text)
            states.append(state)
        return states

    #get name,state
    def get_sensor_infomations_by_type(self, type):
        # return name and state {[name,state],[..]}
        states = []
        root = self.get_states_tree()
        for item in root.findall("item"):
            if type == root.find("type").text:
                state = []
                state.append(item.find("name").text)
                state.append(item.find("state").text)
                states.append(state)
        return states


    #get name,state and type
    def get_all_sensor_informations(self):
        #return name,state and type {[name,state,type],[..]}
        states = []
        root = self.get_states_tree()
        for item in root.findall("item"):
            state = []
            state.append(item.find("name").text)
            state.append(item.find("state").text)
            state.append(item.find("type").text)
            states.append(state)
        return states

    #get sensor state by name
    def get_sensor_state(self, name):
        root = self.get_state_tree_by_name(name)
        if root == None:
            print "No sensor name match"
            return
        else:
            return root.find("state").text

    #get sensor type  by name
    def get_sensor_type(self, name):
        root = self.get_state_tree_by_name(name)
        if root == None:
            print "No sensor name match"
            return
        else:
            return root.find("type").text

##  set sensor state

    # set sensor state by name
    def set_sensor_state(self, name, state):
        if requests.put(self.url + "/rest/items/"+ name + "/state", state).status_code == 200:
            return "SUCCESS"
        return "ERROR"

    # unusable ----- BECAUSE TYPE IN CONFIG ### TYPE FROM REAL WORLD
    # # set sensors state by type
    # def set_sensors_state_by_type(self, type, state):
    #     pass
    #
    # #switch state of switch, light, door,...
    # def switch_sensors_state(self, type, state):
    #     pass