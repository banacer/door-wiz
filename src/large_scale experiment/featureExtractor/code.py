from serial import Serial
import time
import sys

def calibrate(byte):
    while ord(byte) != ord('\n'):
        byte = ser.read()      
    print "yes!"
   
ser = Serial('/dev/ttyACM0',9600)
count  = 0
lastcount = 0
data = ["UT","UL","UR"]
print data
data = []

calibrate(ser.read())
print "yes"
while True:       
    bytes = ser.read(7)
    for i in range(0,3):                    
        a = ord(bytes[2*i])
        b = ord(bytes[2*i  + 1])
        val  = a | (b << 8)
        data.append(val)
    t = time.time()
    print t," : ",data
    data = []
    calibrate(bytes[6])
         