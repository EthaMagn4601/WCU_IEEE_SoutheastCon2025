import RPi.GPIO as GPIO
import time

# Setup
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
BUTTON_PIN = 17
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Pull-down resistor

# Global variables
main_running = True
a_count_running = False

# Interrupt callback function
def button_callback(channel):
    global main_running, a_count_running
    count = 0
    main_running = False  # Stop the main loop
    a_count_running = True  # Start the counting loop
    print("Button pressed!")
    
    try:
        while a_count_running == True:
            print(f"Active count: {count}")
            print(a_count_running)
            count += 1
            time.sleep(1)
    except KeyboardInterrupt:
        a_count_running = False
    print("Counting ended.")

GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=button_callback, bouncetime=300)

try:
    count = 0
    print("Waiting for button press...")
    while main_running == True:
        print(f"Idle Count: {count}")
        count += 1
        time.sleep(0.001)  # Keep the script running
        if count == 15000:
            main_running = False
except KeyboardInterrupt:
    print("Keyboard Interrupt received.")
    a_count_running = False  # Stop the counting loop
    main_running = False  # Stop the main loop
    print("Exiting...")
finally:
    GPIO.cleanup()  # Clean up GPIO on exit