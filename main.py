import netman
import time
from umqttsimple import MQTTClient
from time import sleep
from machine import Pin, PWM
import utime

country = 'GB'
ssid = 'VFAST SG '
password = '95281018'
wifi_connection = netman.connectWiFi(ssid,password,country)

#mqtt config
mqtt_server = '192.168.0.163'
client_id = 'PicoW'
user_t = 'homeassistant'
password_t = 'iiteCheesil5iehesaisohra5joixisohp2do7nee7Wiethai8Aep5ayepa2aaPa'
topic_pub = 'hello'

last_message = 0
message_interval = 5
counter = 0

#MID = 5750
#MIN = 1500
#MAX = 8000

#led = Pin(25,Pin.OUT)
#pwm = PWM(Pin(15))
servo_pin=16                            #This needs to be changed to the pin out where the signal is going into from the servo (I used GP16 on the pico W)
servo= Pin(servo_pin, Pin.OUT)
servo = PWM(Pin(16))                    #This needs to be changed to the pin out where the signal is going into from the servo (I used GP16 on the pico W)
servo.freq(50)

def light_on():              
    servo.duty_u16(3000)

def light_off():
    servo.duty_u16(5650)
    
def light_idle():
    servo.duty_u16(4350)

light_idle()

#pwm.freq(50)
#pwm.duty_ns(MID)

#MQTT connect
def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, user=user_t, password=password_t, keepalive=60)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

#reconnect & reset
def reconnect():
    print('Failed to connected to MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

def callback(topic, msg): 
    print((topic, msg))
    msg = msg.decode('UTF-8')
    if msg == 'on':
        print("light off")
        light_off()
        utime.sleep(1)
        light_idle()
    if msg == 'off':
        print("light on")
        light_on()
        utime.sleep(1)
        light_idle()
    
try:
    client = mqtt_connect()
except OSError as e:
    reconnect()
while True:
    client.set_callback(callback)
    client.subscribe(topic_pub)
    time.sleep(1)

