import re
from serial import Serial
import time

ser = Serial('/dev/ttyACM0',9600)
count = 0
while True:       
    line = ser.readline()    
    print line