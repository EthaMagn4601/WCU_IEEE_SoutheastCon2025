from machine import Pin, PWM, I2C
import time
from bno055 import *
import functions as func

time.sleep(0.5) # Initial 500ms sleep allows for BNO055 chip to fully power up
func.rover_startup()

# while True:
#         func.rover_heading_test()
#         time.sleep(0.1)
    

delay_time = 1
time_step = 0.001 #Global time.sleep() value, make sure value matches in functions.py
rover_throttle_pct = 40

    
try: 
    while True:

        func.rover_hard_right(rover_throttle_pct, 0.5)
        func.rover_stop(1)
        func.rover_backward(rover_throttle_pct, 0.2)
        func.rover_stop(1)
        
        func.rover_forward(rover_throttle_pct, 1.25)
        func.rover_stop(1)
        
        func.rover_hard_right(rover_throttle_pct, 0.5)
        func.rover_stop(1)
        
        func.rover_hard_left(rover_throttle_pct, 1)
        func.rover_stop(1)
        
        func.rover_backward(rover_throttle_pct, 0.25)
        func.rover_stop(1)
        func.rover_right(rover_throttle_pct, 180)
        func.rover_stop(1)
        func.rover_backward(rover_throttle_pct, 0.25)
        func.rover_stop(1)
        func.rover_hard_right(rover_throttle_pct, 1.2)
        func.rover_stop(1)
        
#         func.rover_right_press(rover_throttle_pct, 10)
        func.rover_stop(1) 
        func.rover_hard_left(rover_throttle_pct, 0.8)
        func.rover_stop(1)
        func.rover_backward(rover_throttle_pct, 0.2)
        func.rover_stop(1)
       
        func.rover_forward(rover_throttle_pct, 1.25)
        func.rover_stop(1)
        
        func.rover_backward(rover_throttle_pct, 0.3)
        func.rover_stop(1)
        func.rover_right(rover_throttle_pct, 90)
        func.rover_stop(1)
        func.rover_left(rover_throttle_pct, 90)
        func.rover_stop(1)
        func.rover_backward(rover_throttle_pct, 1)
        func.rover_stop(1)
        
        
        
        
        #Heading tester code
        while True:
            func.rover_heading_test()
            time.sleep(0.1)

except KeyboardInterrupt:
    func.rover_face_heading(rover_throttle_pct, 0)
    func.rover_stop(1)
    print("Program Stopped")
    while True:
        time.sleep(1)

finally:
    func.rover_stop(1)
    print("Program closing out")