from machine import Pin, PWM, I2C # type: ignore
import time
from bno055 import * # type: ignore

# time.sleep(0.5) # Initial 500ms sleep allows for BNO055 chip to fully power up

i2c = I2C(0, sda=Pin(16), scl=Pin(17))
imu = BNO055(i2c) # type: ignore

time_step = 0.001 #Global time.sleep() value, make sure value matches in main.py
fast_correction_dc = 15
acc_correction_dc = 8
c_error_val = 2

#Front left motor pin declaration
ena1 = PWM(Pin(0)) #GPIO 0 = ena1
ena1.freq(1000) 
in1 = Pin(1, Pin.OUT) #GPIO 1 = In1
in2 = Pin(2, Pin.OUT) #GPIO 2 = In2

#Back left motor pin declaration
ena2 = PWM(Pin(3)) #GPIO 3 = ena2
ena2.freq(1000)
in3 = Pin(4, Pin.OUT) #GPIO 4 = In3
in4 = Pin(5, Pin.OUT) #GPIO 5 = In4

#Front right motor pin declaration
ena3 = PWM(Pin(6)) #GPIO 6 = ena3
ena3.freq(1000)
in5 = Pin(7, Pin.OUT) #GPIO 7 = In5
in6 = Pin(8, Pin.OUT) #GPIO 8 = In6

#Back right motor pin declaration
ena4 = PWM(Pin(9)) #GPIO 9 = ena4
ena4.freq(1000)
in7 = Pin(10, Pin.OUT)
in8 = Pin(11, Pin.OUT)

def PWM_th(duty_cycle_percent):
    duty_cycle = int((duty_cycle_percent / 100) * 65536)
    return duty_cycle

def rover_startup():
    heading = imu.euler()
    heading_deg = round(heading[0])
    print("Rover starting")
    
    time_int = time.time()
    time_now = 0
    delta_t = 0
    
    while delta_t < 1:
        heading = imu.euler()
        heading_deg = round(heading[0])
        
        if (heading_deg > 1) and (heading_deg < 359):
            print("IMU isn't reading properly")
            while True:
                heading = imu.euler()
                heading_deg = round(heading[0])
                print(f"Heading: {heading_deg}")
                time.sleep(1)
        elif (heading_deg < 359) and (heading_deg > 350):
            print("IMU isn't reading properly")
            while True:
                heading = imu.euler()
                heading_deg = round(heading[0])
                print(f"Heading: {heading_deg}")
                time.sleep(1)
        
        time_now = time.time()
        delta_t = time_now - time_int
        time.sleep(0.01)
        print(f"Time_int = {time_int}")
        print(f"Time_now = {time_now}")
        print(f"Delta_t = {delta_t}")
        
    print("Rover properly started")

def rover_heading_test():
    heading = imu.euler()
    heading_deg = round(heading[0])
    print(f"Rover Heading: {heading_deg}")
    time.sleep(0.01)
    
def rover_stop(off_t):
    in1.low()
    in2.low()
    ena1.duty_u16(0)
    
    in3.low()
    in4.low()
    ena2.duty_u16(0)
    
    in5.low()
    in6.low()
    ena3.duty_u16(0)
    
    in7.low()
    in8.low()
    ena4.duty_u16(0)
    
    heading = imu.euler()
    heading_deg = round(heading[0])
    print(f"Rover stopped at: {heading_deg}")
    
    time.sleep(off_t)

def rover_forward(rover_throttle_pct, run_t):
    rover_speed = PWM_th(rover_throttle_pct)
    #Spin front left forward
    in1.high()
    in2.low()
    ena1.duty_u16(rover_speed)
    
    #Spin back left forward
    in3.high()
    in4.low()
    ena2.duty_u16(rover_speed)
    
    #Spin front right forward
    in5.high()
    in6.low()
    ena3.duty_u16(rover_speed)
    
    #Spin back right forward
    in7.high()
    in8.low()
    ena4.duty_u16(rover_speed)
    time.sleep(run_t)
    
def rover_backward(rover_throttle_pct, run_t):
    rover_speed = PWM_th(rover_throttle_pct)
    
    in1.low()
    in2.high()
    ena1.duty_u16(rover_speed)
    
    in3.low()
    in4.high()
    ena2.duty_u16(rover_speed)
    
    in5.low()
    in6.high()
    ena3.duty_u16(rover_speed)
    
    in7.low()
    in8.high()
    ena4.duty_u16(rover_speed)
    time.sleep(run_t)

def rover_left_correction(rover_dutycycle):
    rover_speed = PWM_th(rover_dutycycle)
    
    in1.low()
    in2.high()
    ena1.duty_u16(rover_speed)
    
    in3.low()
    in4.high()
    ena2.duty_u16(rover_speed)
    
    in5.high()
    in6.low()
    ena3.duty_u16(rover_speed)
    
    in7.high()
    in8.low()
    ena4.duty_u16(rover_speed)
    
def rover_right(rover_throttle_pct, deg_to_turn_to):
    rover_speed = PWM_th(rover_throttle_pct)
    
    in1.high()
    in2.low()
    ena1.duty_u16(rover_speed)
    
    in3.high()
    in4.low()
    ena2.duty_u16(rover_speed)
    
    in5.low()
    in6.high()
    ena3.duty_u16(rover_speed)
    
    in7.low()
    in8.high()
    ena4.duty_u16(rover_speed)
    
    heading = imu.euler()
    heading_deg = round(heading[0])
    initial_heading = heading_deg
    
    if deg_to_turn_to == 0:
        if heading_deg == 0:
            rover_stop(1)
            return
        else:
            while heading_deg >= initial_heading:
                heading = imu.euler()
                heading_deg = round(heading[0])
                time.sleep(time_step)
#                 print("Right Case 1")
#                 print(f"Heading: {heading_deg}")
            rover_stop(0.1)
            
            heading = imu.euler()
            heading_deg = round(heading[0])
            
            while heading_deg > (deg_to_turn_to + 10):
                rover_left_correction(fast_correction_dc)
                heading = imu.euler()
                heading_deg = round(heading[0])
                time.sleep(time_step)
#                 print("Right Case 2")
#                 print(f"Heading: {heading_deg}")
            rover_stop(0.1)

                
            while (heading_deg > deg_to_turn_to + c_error_val) and heading_deg < 360:
                rover_left_correction(acc_correction_dc)
                heading = imu.euler()
                heading_deg = round(heading[0])
                time.sleep(time_step)
#                 print("Right Case 3")
#                 print(f"Heading: {heading_deg}")
            rover_stop(0.1)

            
    elif deg_to_turn_to <= initial_heading:
        # while loop will make the robot go past 360/0 threshold
        while heading_deg >= initial_heading:
            heading = imu.euler()
            heading_deg = round(heading[0])
            time.sleep(time_step)
#             print("Right Case 4")
#             print(f"Heading: {heading_deg}")
        
        while heading_deg < deg_to_turn_to:
            heading = imu.euler()
            heading_deg = round(heading[0])
            time.sleep(time_step)
#             print("Right Case 5")
#             print(f"Heading: {heading_deg}")
        rover_stop(0.1)
        
        heading = imu.euler()
        heading_deg = round(heading[0])
        
        while heading_deg > (deg_to_turn_to + 10):
            rover_left_correction(fast_correction_dc)
            heading = imu.euler()
            heading_deg = round(heading[0])
            time.sleep(time_step)
#             print("Right Case 6")
#             print(f"Heading: {heading_deg}")
        rover_stop(0.1)

            
        while (heading_deg > deg_to_turn_to + c_error_val) and (heading_deg < 360):
            rover_left_correction(acc_correction_dc)
            heading = imu.euler()
            heading_deg = round(heading[0])
            time.sleep(time_step)
#             print("Right Case 7")
#             print(f"Heading: {heading_deg}")
        rover_stop(0.1)
    
    else:
        while heading_deg < deg_to_turn_to:
            heading = imu.euler()
            heading_deg = round(heading[0])
            time.sleep(time_step)
        rover_stop(0.1)
        
        heading = imu.euler()
        heading_deg = round(heading[0])
        
        while heading_deg > (deg_to_turn_to + 10):
            rover_left_correction(fast_correction_dc)
            heading = imu.euler()
            heading_deg = round(heading[0])
            time.sleep(time_step)
            print("Right Case 6")
            print(f"Heading: {heading_deg}")
        rover_stop(0.1)
            
        while (heading_deg > deg_to_turn_to + c_error_val) and (heading_deg < 360):
            rover_left_correction(acc_correction_dc)
            heading = imu.euler()
            heading_deg = round(heading[0])
            time.sleep(time_step)
            print("Right Case 7")
            print(f"Heading: {heading_deg}")
        rover_stop(0.1)
        
        
def rover_right_correction(rover_dutycycle):
    rover_speed = PWM_th(rover_dutycycle)
    
    in1.high()
    in2.low()
    ena1.duty_u16(rover_speed)
    
    in3.high()
    in4.low()
    ena2.duty_u16(rover_speed)
    
    in5.low()
    in6.high()
    ena3.duty_u16(rover_speed)
    
    in7.low()
    in8.high()
    ena4.duty_u16(rover_speed)
    
def rover_left(rover_throttle_pct, deg_to_turn_to):
    rover_speed = PWM_th(rover_throttle_pct)
    
    in1.low()
    in2.high()
    ena1.duty_u16(rover_speed)
    
    in3.low()
    in4.high()
    ena2.duty_u16(rover_speed)
    
    in5.high()
    in6.low()
    ena3.duty_u16(rover_speed)
    
    in7.high()
    in8.low()
    ena4.duty_u16(rover_speed)
    
    heading = imu.euler()
    heading_deg = round(heading[0])
    
    if heading_deg == 0:
        # if robot is set to turn to 0 degrees and is already at 0 degrees, the robot will not do anything
        if deg_to_turn_to == 0:
            rover_stop()
            return
        else:
            # time.sleep(0.1) spins robot past 0 degrees so that it may behave off of simple degree comparison logic i.e. comparing to see if its value is
            # less than its targeted deg_to_turn_to value
            while heading_deg == 0 or heading_deg == 360 or heading_deg == 1:
                heading = imu.euler()
                heading_deg = round(heading[0])
                time.sleep(0.01)
#                 print("Left Case 1")
#                 print(f"Heading: {heading_deg}")
            time.sleep(0.1)
            
            heading = imu.euler()
            heading_deg = round(heading[0])
            
            while heading_deg > deg_to_turn_to:
                # contiually update heading angle, robot will stop turning left if it has reached or passed targeted deg_to_turn_to_value
                heading = imu.euler()
                heading_deg = round(heading[0])
                time.sleep(time_step)
#                 print("Left Case 2")
#                 print(f"Heading: {heading_deg}")
            # stops robot and sleeps to give the robots momentum time to reach zero
            rover_stop(0.1)

            
            heading = imu.euler()
            heading_deg = round(heading[0])
            
            if heading_deg < deg_to_turn_to:
                # robot spins 
                while heading_deg < (deg_to_turn_to - 10):
                    rover_right_correction(fast_correction_dc)
                    heading = imu.euler()
                    heading_deg = round(heading[0])
                    time.sleep(time_step)
#                     print("Left Case 3")
#                     print(f"Heading: {heading_deg}")
                rover_stop(0.1)
                
                
                while heading_deg < deg_to_turn_to:
                    rover_right_correction(acc_correction_dc)
                    heading = imu.euler()
                    heading_deg = round(heading[0])
                    time.sleep(time_step)
#                     print("Left Case 4")
#                     print(f"Heading: {heading_deg}")
                rover_stop(0.1)
                
                
    elif heading_deg < deg_to_turn_to:
        # while loop that brings robot past 0 deg threshold
        while heading_deg > 0:
            heading = imu.euler()
            heading_deg = round(heading[0])
            time.sleep(time_step)
#             print("Left Case 5")
#             print(f"Heading: {heading_deg}")
        
        heading = imu.euler()
        heading_deg = round(heading[0])
        
        if heading_deg > deg_to_turn_to:
            while heading_deg > deg_to_turn_to:
                # contiually update heading angle, robot will stop turning left if it has reached or passed targeted deg_to_turn_to_value
                heading = imu.euler()
                heading_deg = round(heading[0])
                time.sleep(time_step)
#                 print("Left Case 6")
#                 print(f"Heading: {heading_deg}")
            # stops robot and sleeps to give the robots momentum time to reach zero
            rover_stop(0.1)
            
        
        while heading_deg < (deg_to_turn_to - 10):
            rover_right_correction(fast_correction_dc)
            heading = imu.euler()
            heading_deg = round(heading[0])
            time.sleep(time_step)
#             print("Left Case 7")
#             print(f"Heading: {heading_deg}")
        rover_stop(0.1)
        
                
        while heading_deg < deg_to_turn_to:
            rover_right_correction(acc_correction_dc)
            heading = imu.euler()
            heading_deg = round(heading[0])
            time.sleep(time_step)
#             print("Left Case 8")
#             print(f"Heading: {heading_deg}")
        rover_stop(0.1)
        
        
    else:
        time.sleep(0.1)
        while heading_deg > deg_to_turn_to:
            # contiually update heading angle, robot will stop turning left if it has reached or passed targeted deg_to_turn_to_value
            heading = imu.euler()
            heading_deg = round(heading[0])
            time.sleep(time_step)
#             print("Left Case 9")
#             print(f"Heading: {heading_deg}")
        # stops robot and sleeps to give the robots momentum time to reach zero
        rover_stop(0.1)
        
        
        heading = imu.euler()
        heading_deg = round(heading[0])
        
        if heading_deg < deg_to_turn_to:
                # robot spins 
                while heading_deg < (deg_to_turn_to - 10):
                    rover_right_correction(fast_correction_dc)
                    heading = imu.euler()
                    heading_deg = round(heading[0])
                    time.sleep(time_step)
#                     print("Left Case 10")
#                     print(f"Heading: {heading_deg}")
                rover_stop(0.1)
                
                
                while heading_deg < deg_to_turn_to:
                    rover_right_correction(acc_correction_dc)
                    heading = imu.euler()
                    heading_deg = round(heading[0])
                    time.sleep(time_step)
#                     print("Left Case 11")
#                     print(f"Heading: {heading_deg}")
                rover_stop(0.1)
                
        return
    
def rover_face_heading(rover_throttle_pct, deg_to_turn_to):
    heading = imu.euler()
    heading_deg = round(heading[0])
    
    if (heading_deg == 359) or (heading_deg == 360) or (heading_deg == 0) or (heading_deg == 1) and (deg_to_turn_to == 0):
        return
    if heading_deg >= 180:
        rover_right(rover_throttle_pct, deg_to_turn_to)
    else:
        rover_left(rover_throttle_pct, deg_to_turn_to)
        
def rover_hard_right(rover_throttle_pct, run_t):
    rover_speed = PWM_th(rover_throttle_pct)
    #Spin front left forward
    in1.high()
    in2.low()
    ena1.duty_u16(rover_speed)
    
    #Spin back left backward
    in3.low()
    in4.high()
    ena2.duty_u16(rover_speed)
    
    #Spin front right backward
    in5.low()
    in6.high()
    ena3.duty_u16(rover_speed)
    
    #Spin back right forward
    in7.high()
    in8.low()
    ena4.duty_u16(rover_speed)
    
    time.sleep(run_t)
    
def rover_hard_left(rover_throttle_pct, run_t):
    rover_speed = PWM_th(rover_throttle_pct)
    #Spin front left backward
    in1.low()
    in2.high()
    ena1.duty_u16(rover_speed)
    
    #Spin back left forward
    in3.high()
    in4.low()
    ena2.duty_u16(rover_speed)
    
    #Spin front right forward
    in5.high()
    in6.low()
    ena3.duty_u16(rover_speed)
    
    #Spin back right backward
    in7.low()
    in8.high()
    ena4.duty_u16(rover_speed)
    
    time.sleep(run_t)
    
def rover_right_press(rover_throttle_pct, run_t):
    
    time_int = time.time()
    time_now = 0
    delta_t = 0
    
    while delta_t < run_t:
        rover_forward(rover_throttle_pct, 0.1)
        rover_hard_right(rover_throttle_pct, 0.2)
        
        time_now = time.time()
        delta_t = time_now - time_int
        time.sleep(0.01)