from Mfrc522 import MFRC522 
import utime
from machine import Pin, PWM
from time import sleep 
import network
import _thread
import time
try:
  import usocket as socket
except:
  import socket
  
servo = PWM(Pin(16))
servo.freq(50)


def light_on():
    servo.duty_u16(2900)
    
def light_off():
    servo.duty_u16(4500)
    
def light_idle():
    servo.duty_u16(3700)


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("VFAST SG ","95281018")       # ssid, password
 
# connect the network       
wait = 10
while wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    wait -= 1
    print('waiting for connection...')
    time.sleep(1)
 
# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('wifi connection failed')
else:
    print('connected')
    ip=wlan.ifconfig()[0]
    print('IP: ', ip)
    
 
def web_server():
  if servo.duty_u16() == 4500:
    servo_state = ''
  else:
    servo_state = 'checked'
  html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>
  body{font-family:Arial; text-align: center; margin: 0px auto; padding-top:30px;}
  .switch{position:relative;display:inline-block;width:120px;height:68px}.switch input{display:none}
  .slider{position:absolute;top:0;left:0;right:0;bottom:0;background-color:#ccc;border-radius:34px}
  .slider:before{position:absolute;content:"";height:52px;width:52px;left:8px;bottom:8px;background-color:#fff;-webkit-transition:.4s;transition:.4s;border-radius:68px}
  input:checked+.slider{background-color:#2196F3}
  input:checked+.slider:before{-webkit-transform:translateX(52px);-ms-transform:translateX(52px);transform:translateX(52px)}
  </style><script>function toggleCheckbox(element) { var xhr = new XMLHttpRequest(); if(element.checked){ xhr.open("GET", "/?light=on", true); }
  else { xhr.open("GET", "/?light=off", true); } xhr.send(); }</script></head><body>
  <h1>Pico W IoT Light Control</h1><label class="switch"><input type="checkbox" onchange="toggleCheckbox(this)" %s><span class="slider">
  </span></label></body></html>""" % (servo_state)
  return html
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(5)

 
while True:
    
    try:
        conn, addr = s.accept()
        conn.settimeout(3.0)
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request)
        print('Content = %s' % request)
        light_on = request.find('/?light=on')
        light_off = request.find('/?light=off')
        if servo.duty_u16(4500):
          print('LIGHT ON')
          light_idle
        if servo.duty_u16(4500):
          print('LIGHT OFF')
          light_idle
        response = web_server()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except OSError as e:
        conn.close()
        print('Connection closed')
