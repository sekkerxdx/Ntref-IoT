import time
import Adafruit_DHT
from beebotte import *

bbt = BBT('BME6UPxl7TJGoQKhYtFxoNpc', 'otw4bkPmc0SbTsCCKdTPY98kJf817tl6')

period = 300 
pin = 11

temp_resource   = Resource(bbt, 'IoT_House', 'temperature')
humid_resource  = Resource(bbt, 'IoT_House', 'humidity')

def run():
  while True:
      
    humidity, temperature = Adafruit_DHT.read_retry( Adafruit_DHT.DHT11, pin )
    
    if humidity is not None and temperature is not None:
        print ("Temp={0:f}*C Humidity={1:f}%".format(temperature, humidity))
        print (temperature)
        try:
          temp_resource.write(temperature)
          humid_resource.write(humidity)
            
        except Exception:
          print ("Error de conexion con Beebotte")
    else:
        print ("Falla con adafruit")
    time.sleep( period )

run()