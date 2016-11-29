from influxdb import InfluxDBClient

class Data_recorder(object):
    list_platforms = []
    db_client = None

    def __init__(self, list_platforms):
        self.db_client = self.influxdb_init()
        self.list_platforms = list_platforms

    def influxdb_init(self):
        host='localhost'
        # host = os.environ['INFLUX_HOST']  # influxdb host name
        port = 8086
        user = 'root'
        password = 'root'
        dbname = 'ipd'
        dbuser = ''
        dbuser_password = ''
        client = InfluxDBClient(host, port, user, password, dbname)
        client.drop_database(dbname)  # 2.10 delete_database / 2.12: drop_database
        client.create_database(dbname)
        return client

    def update_data(self):
        for platform in self.list_platforms:
            if platform.driver.check_status() == True:
                items = platform.driver.get_all_sensors_infomation()
                for item in items:
                    json_body = [
                        {
                            "measurement": item[0],
                            "tags": {
                                "platform": platform.platform
                            },
                            "fields": {
                                "soft_name": item[0],
                                "state": item[1],
                                "type": item[2],
                            }
                        }
                    ]
                    self.db_client.write_points(json_body)


