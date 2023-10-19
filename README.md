# ha_hdhr_to_mqtt

## What this does
This "app" will send information to a Home Assistant instance via MQTT. 

Example sensor output:
```
{
    "topic": "tuner0/sensor", 
    "payload": {
        "Resource": "tuner0",
        "VctNumber": "9.1",
        "VctName": "FOX-9",
        "Frequency": 563000000,
        "SignalStrengthPercent": 83,
        "SignalQualityPercent": 76,
        "SymbolQualityPercent": 100,
        "TargetIP": "192.168.0.1",
        "NetworkRate": 3001760,
        "status": "In Use",
        "ReportTime": "Thu October 19 09:24"
    }
}
```

### Home Assistant Discovery Information
This app uses Home Assistant's Discovery mode for MQTT. An example discovery config object is
```
sig_strength_config_object = {
    "name": "Signal Strength",
    "unique_id": signal_strength_unique_id,
    "state_topic": state_topic,
    "value_template": "{{ value_json.payload.SignalStrengthPercent }}",
    "unit_of_measurement": "%",
    "device": device_dict,
}
```
where `device_dict` is defined as 
```
device_dict = {
    "identifiers": f"HDHR_{tunerid}",
    "manufacturer": "Silicon Dust",
    "name": f"HD Home Run {tunerid}",
}
```
. The discovery topic is then sent to Home Assistant as
```
signal_strength_discovery_topic = f"{home_assistant_discovery_root}/{signal_strength_unique_id}/config"
```
where `home_assistant_discovery_root` is defined as `homeassistant/sensor` and `signal_strength_unique_id` is defined as `f"hdhr_{tunerid}_signal_strength"`

## Docker Build and Run
First, create a .env file with the following variables:
```
MQTT_HOST="<ip_of_the_mqtt_broker>"
MQTT_PORT="<port_of_the_mqtt_broker>"
MQTT_USER="<mqtt_username_to_send_messages_to_home_assistant>"
MQTT_PASSWORD="<password_for_mqtt_user>"
HDHR_IP="<ip_of_the_hd_homerun_device>"
```
Then, build the docker image:
```
docker build -t ha_hdhr_to_mqtt:latest .
```
and run it:
```
docker-compose up -d
```
