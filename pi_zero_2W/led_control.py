import RPi.GPIO as GPIO
import time

# Setup
LED_PIN = 4  # GPIO pin number for the onboard LED

# Clean up any existing GPIO setting

# Set up GPIO
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
GPIO.setup(LED_PIN, GPIO.OUT)  # Set the LED pin as output

try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)  # Turn LED on
        print("High")
        time.sleep(0.01)  # Wait for 1 second
        GPIO.output(LED_PIN, GPIO.LOW)  # Turn LED off
        print("Low")
        time.sleep(0.01)  # Wait for 1 second
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()  # Clean up GPIO settings