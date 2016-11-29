from openhab import openhab_driver as oh
from home_assistant import home_assitant as ha
class Drive_client():
    """ docString for Client"""
    driver = None
    host = None
    port = None
    platform = None
    def __init__(self, platform, host = None, port = None):
        self.platform = platform
        self.host = host
        self.port = port
        self.__setup()
    def __setup(self):
        if self.platform == "openhab":
            self.host = self.host if self.host is not None else "localhost"
            self.port = self.port if self.port is not None else "8080"
            self.driver = oh(self.host, self.port)
            print "set driver OH"
        elif self.platform == "home-assistant":
            self.host = self.host if self.host is not None else "localhost"
            self.port = self.port if self.port is not None else "8123"
            self.driver = ha(self.host, self.port)
            print "set driver HA"