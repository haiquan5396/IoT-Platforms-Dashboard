###DataBase Structure (JSON template)
```
json_body = [
    {
        "measurement": name, // name in openhab, entity_id in home_assistant
        "tags": {
            "platform": "openhab"  or "home-assistant"
        },
        "fields": {
            "soft_name": name,  // name in "openhab"
            "type" : type,      // type of sensor
            "state" : state,    //state
        }
    }
]
```