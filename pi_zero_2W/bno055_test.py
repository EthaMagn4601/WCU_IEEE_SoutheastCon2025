import time
import board
import busio
from adafruit_bno055 import BNO055

i2c = busio.I2C(board.SCL, board.SDA)
sensor = BNO55(i2c)

time.sleep(1)

try:
    while True:
        heading, roll, pitch = sensor.euler
        print(f"Heading: {heading:.2f}, Roll: {roll:.2f}, Pitch:{pitch:.2f}")
        
        accel = sensor.acceleration
        gyro = sensor.gyroschope
        mag = sensor.magnetic
        
        print(f"Accelerometer: {accel}, Gyroscope {gyro}, Magnetometer: {mag}")
        
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting Program.")