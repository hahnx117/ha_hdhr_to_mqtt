import requests
from pprint import pprint
import paho.mqtt.client as mqtt
import json
import socket
from datetime import datetime
import time
import os

HDHR_IP = os.environ['HDHR_IP']
BASEURL = f"http://{HDHR_IP}"

## CREATE DISCOVERY OBJECTS AND TOPICS ##


def register_devices_using_discovery(tunerid, mqtt_client):

    home_assistant_discovery_root = "homeassistant/sensor"
    state_topic = f"{tunerid}/sensor"

    report_time_unique_id = f"{tunerid}_report_time"
    signal_quality_unique_id = f"{tunerid}_sig_qual"
    signal_strength_unique_id = f"{tunerid}_sig_strength"
    symbol_quality_unique_id = f"{tunerid}_symb_qual"
    target_ip_unique_id = f"{tunerid}_target_ip"
    vct_name_unique_id = f"{tunerid}_vct_name"
    vct_number_unique_id = f"{tunerid}_vct_number"
    status_unique_id = f"{tunerid}_status"

    report_time_discovery_topic = f"{home_assistant_discovery_root}/{report_time_unique_id}/config"
    signal_quality_discovery_topic = f"{home_assistant_discovery_root}/{signal_quality_unique_id}/config"
    signal_strength_discovery_topic = f"{home_assistant_discovery_root}/{signal_strength_unique_id}/config"
    symbol_quality_discovery_topic = f"{home_assistant_discovery_root}/{symbol_quality_unique_id}/config"
    target_ip_discovery_topic = f"{home_assistant_discovery_root}/{target_ip_unique_id}/config"
    vct_name_discovery_topic = f"{home_assistant_discovery_root}/{vct_name_unique_id}/config"
    vct_number_discovery_topic = f"{home_assistant_discovery_root}/{vct_number_unique_id}/config"
    status_discovery_topic = f"{home_assistant_discovery_root}/{status_unique_id}/config"


    device_dict = {
        "identifiers": f"HDHR_{tunerid}",
        "manufacturer": "Silicon Dust",
        "name": f"HD Home Run {tunerid}",
    }

    report_time_config_object = {
        "name": "Timestamp",
        "unique_id": report_time_unique_id,
        "state_topic": state_topic,
        "value_template": "{{ value_json.payload.ReportTime }}",
        "device": device_dict,
    }

    sig_qual_config_object = {
        "name": "Signal Quality",
        "unique_id": signal_quality_unique_id,
        "state_topic": state_topic,
        "value_template": "{{ value_json.payload.SignalQualityPercent }}",
        "unit_of_measurement": "%",
        "device": device_dict,
    }

    sig_strength_config_object = {
        "name": "Signal Strength",
        "unique_id": signal_strength_unique_id,
        "state_topic": state_topic,
        "value_template": "{{ value_json.payload.SignalStrengthPercent }}",
        "unit_of_measurement": "%",
        "device": device_dict,
    }

    symbol_quality_config_object = {
        "name": "Symbol Quality Strength",
        "unique_id": symbol_quality_unique_id,
        "state_topic": state_topic,
        "value_template": "{{ value_json.payload.SymbolQualityPercent }}",
        "unit_of_measurement": "%",
        "device": device_dict,
    }

    target_ip_config_object = {
        "name": "Target IP",
        "unique_id": target_ip_unique_id,
        "state_topic": state_topic,
        "value_template": "{{ value_json.payload.TargetIP }}",
        "device": device_dict,
    }

    vct_name_config_object = {
        "name": "VCT Name",
        "unique_id": vct_name_unique_id,
        "state_topic": state_topic,
        "value_template": "{{ value_json.payload.VctName }}",
        "device": device_dict,
    }

    vct_number_config_object = {
        "name": "VCT Number",
        "unique_id": vct_number_unique_id,
        "state_topic": state_topic,
        "value_template": "{{ value_json.payload.VctNumber }}",
        "device": device_dict,
    }

    status_config_object = {
        "name": "Status",
        "unique_id": status_unique_id,
        "state_topic": state_topic,
        "value_template": "{{ value_json.payload.status }}",
        "device": device_dict,
    }

    try:
        mqtt_client.publish(report_time_discovery_topic, json.dumps(report_time_config_object), qos=1, retain=True)
        mqtt_client.publish(signal_quality_discovery_topic, json.dumps(sig_qual_config_object), qos=1, retain=True)
        mqtt_client.publish(signal_strength_discovery_topic, json.dumps(sig_strength_config_object), qos=1, retain=True)
        mqtt_client.publish(symbol_quality_discovery_topic, json.dumps(symbol_quality_config_object), qos=1, retain=True)
        mqtt_client.publish(target_ip_discovery_topic, json.dumps(target_ip_config_object), qos=1, retain=True)
        mqtt_client.publish(vct_name_discovery_topic, json.dumps(vct_name_config_object), qos=1, retain=True)
        mqtt_client.publish(vct_number_discovery_topic, json.dumps(vct_number_config_object), qos=1, retain=True)
        mqtt_client.publish(status_discovery_topic, json.dumps(status_config_object), qos=1, retain=True)

    except Exception as e:
        print(e)


def get_status():
    """Gets the status of the HD HomeRun."""
    url = f"{BASEURL}/status.json"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

def num_tuners(status):
    """Returns the number of tuners available."""
    return len(status)

def tuners_active(status):
    """Determins how many tuners are currently active."""
    tuners_active = 0
    
    for i in status:
        if len(i) != 1:
            tuners_active += 1

    return tuners_active


if __name__ == "__main__":
    status = get_status()

    #print(f"Number of tuners on device: {num_tuners(status)}")
    #print("\n")
    #print(f"Tuners active: {tuners_active(status)}")


    data_dict = {
        'Resource': '',
        'VctNumber': "Unavailable",
        'VctName': "Unavailable", 
        'Frequency': "Unavailable",
        'SignalStrengthPercent': 0,
        'SignalQualityPercent': 0,
        'SymbolQualityPercent': 0,
        'TargetIP': "Unavailable",
        'NetworkRate': "Unavailable",
    }

    mqtt_host = os.environ['MQTT_HOST']
    mqtt_port = os.environ['MQTT_PORT']
    mqtt_user = os.environ['MQTT_USER']
    mqtt_password = os.environ['MQTT_PASSWORD']

    hostname = socket.gethostname()


    client = mqtt.Client()
    client.username_pw_set(mqtt_user, mqtt_password)
    client.connect(mqtt_host, int(mqtt_port))
    client.loop_start()


    while True:
        status = get_status()
        for i in status:
            register_devices_using_discovery(i['Resource'], client)

            i['ReportTime'] = datetime.now().strftime("%a %B %d %H:%M")
            sensor_topic = f"{i['Resource']}/sensor"
            status_topic = f"{i['Resource']}/status"
            topic_dict = {'topic': sensor_topic, 'payload': {}}
            
            if len(i) > 2:
                device_status = "In Use"
                topic_dict['payload'] = i
                topic_dict['payload']['status'] = 'In Use'
                sensor_payload = json.dumps(topic_dict)
                client.publish(sensor_topic, sensor_payload, qos=1, retain=True)
                client.publish(status_topic, device_status, qos=1, retain=True)

            #    pprint(topic_dict)
            else:
                topic_dict['payload'] = data_dict
                topic_dict['payload']['Resource'] = i['Resource']
                device_status = 'Not In Use'
                sensor_payload = json.dumps(topic_dict)
                client.publish(sensor_topic, sensor_payload, qos=1, retain=True)
                client.publish(status_topic, device_status, qos=1, retain=True)

            #    pprint(topic_dict)
            #print('\n')
        
            topic_dict = None
        time.sleep(15)
