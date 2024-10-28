import time

count = 0

try:
    while True:
        print(f"Count: {count}")
        count = count+1
        time.sleep(1)
        
except KeyboardInterrupt:
    print("\n--Closing--")
