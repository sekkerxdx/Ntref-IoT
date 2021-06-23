import time
import requests
import math
import random
import Adafruit_DHT
import RPi.GPIO as GPIO

pin1 = 16
pin2 = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)

TOKEN = "BBFF-dA2bHqwnRuXFOG2rMW27oVsNFgyBvk" 
DEVICE_LABEL = "Monitoreo"  
VARIABLE_LABEL_1 = "Temperatura"  
VARIABLE_LABEL_2 = "Humedad"  
VARIABLE_LABEL_3 = "Posicion"  


def build_payload(variable_1, variable_2, variable_3):
    
    sensor1 = Adafruit_DHT.DHT11
    ventilador = GPIO.PWM(pin2, 0.5)
    
    humidity, temperature = Adafruit_DHT.read_retry(sensor1, pin1)
    print(temperature , humidity)
    
    if temperature >= 30.00:
        ventilador.start(1)
    else:
        ventilador.stop()
    
    value_1 = temperature
    value_2 = humidity

    lat = random.randrange(34, 36, 1) + \
        random.randrange(1, 1000, 1) / 1000.0
    lng = random.randrange(-83, -87, -1) + \
        random.randrange(1, 1000, 1) / 1000.0
    payload = {variable_1: value_1,
               variable_2: value_2,
               variable_3: {"value": 1, "context": {"lat": lat, "lng": lng}}}

    return payload


def post_request(payload):
    
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True


def main():
    payload = build_payload(
        VARIABLE_LABEL_1, VARIABLE_LABEL_2, VARIABLE_LABEL_3)

    print("[INFO] Attemping to send data")
    post_request(payload)
    print("[INFO] finished")


if __name__ == '__main__':
    while (True):
        main()
        time.sleep(300)
