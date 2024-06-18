#!/usr/bin/env python3
import serial
import time

ser1 = serial.Serial('/dev/ttyACM0', 115200, timeout=1.0)
ser2 = serial.Serial('/dev/ttyACM1', 74880, timeout=1.0)
time.sleep(3)
ser1.reset_input_buffer()
ser2.reset_input_buffer()
print("Serial OK")

try:
    while True:
        if ser1.inWaiting() > 0:
            line1 = ser1.readline().decode('utf-8').rstrip()
            print("ser1: "+line1)
        if ser2.inWaiting() > 0:
            line2 = ser2.readline().decode('utf-8').rstrip()
            print("ser2: "+line2)
except KeyboardInterrupt:
    print("Close Serial Communication")
    ser1.close()
    ser2.close()
    