import time
import cv2
import serial
import random


from testing import ObjectDetection
from camera import BUFFER, get_image
from remap2 import remap_coor


import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

def clear_buffers():
    if ser.isOpen():
        ser.flushInput()  # Clear input buffer
        ser.flushOutput() # Clear output buffer
        print("Serial buffers cleared.")
    else:
        print("Serial port is not open.")

ins = ObjectDetection(conf_thres = 0.1)

wireless_charger_status = False

def terminate_script():
    global should_continue
    # should_continue = False
    pass  


# For debug purpose only uncomment this one
# cnt = 0


ser = serial.Serial(
    port='/dev/ttyUSB0',  # Replace with the correct USB port for the Arduino
    baudrate=115200,
    timeout=1  # Timeout for read operations, in seconds
)

def clear_buffers():
    if ser.isOpen():
        ser.flushInput()  # Clear input buffer
        ser.flushOutput() # Clear output buffer
        print("Serial buffers cleared.")
    else:
        print("Serial port is not open.")

def neighbor(x,y):
    return [(x+1,y), (x+1, y+1), (x+1, y-1), (x,y), (x,y+1), (x, y-1), (x-1,y+1), (x-1,y), (x-1,y-1)]
time.sleep(2)


should_continue = True

def run_script():
    global ins, should_continue
    CAMID = "/dev/video2"
    idx = 0
    cache = {}
    while should_continue:
        new_cache = {}
        idx += 1
        if idx == BUFFER + 1:
            idx = 1

        # This is for testing only, remove the cnt for prod
        # if cnt == 5:
        #     break
        st = time.time()
        get_image(CAMID, 2)
        img_path = f"obj{idx}cam2.jpg"
        image = cv2.imread(img_path)

        res = ins.detect(img_path, idx, 2)

        # Mapping the center of phone coordinate back to image
        print(res)
        fin = []
        for i in res:
            print(i)
            temp = remap_coor(i[0], i[1])

            if -2 <= temp[0] < 0:
                temp[0] = 0
            if 15 < temp[0] <= 17:
                temp[0] = 15
            # Moveable from 0-11 for x-axis
            key = f"{temp[0]},{temp[1]}"
            if key not in cache:
                # Filter by offset size of box 
                if 15 >= temp[0] >= 0 and 25 >= temp[1] >= 0:
                    fin.append(temp)

            for i in neighbor(temp[0], temp[1]):
                key = f"{i[0]},{i[1]}"
                new_cache[key] = 0

        cache.clear()
        cache = new_cache.copy()
        new_cache.clear()

        print(f"Done in {time.time()-st} s")

        if len(fin):
            chosen = random.choice(fin)
            # The string to send to the Arduino
            data_to_send = f"{chosen[0]},{chosen[1]}"

            # # Check if serial is open and write data
            if ser.isOpen():
                clear_buffers()
                ser.write(data_to_send.encode())  # Encode string to bytes
                print(f"Sent '{data_to_send}' to Arduino.")
            else:
                print("Can't open serial port.")


        time.sleep(10)

def on_wireless_charger_status_change(event):
    global wireless_charger_status
    wireless_charger_status = True if event.data else False
    if wireless_charger_status:
        run_script()
    else:
        terminate_script()
    print(f"WirelessCharging status has changed to: {wireless_charger_status}")

def initialize_firebase():
    # Assuming you've already downloaded your Firebase service account key
    cred = credentials.Certificate("intellidesk-174c9-firebase-adminsdk-garkf-abe9a9fb75.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://intellidesk-174c9-default-rtdb.asia-southeast1.firebasedatabase.app/"
    })
    return db.reference()

# Initialize the database reference
db = initialize_firebase()

# Setting up the listener
wireless_charging_ref = db.child('Controls').child('ChargingCamera')
wireless_charging_ref.listen(on_wireless_charger_status_change) 

try:
    while True:
        pass
except KeyboardInterrupt:
    # Reset to origin
    data_to_send = f"{0},{0}"

    # # Check if serial is open and write data
    if ser.isOpen():
        clear_buffers()
        ser.write(data_to_send.encode())  # Encode string to bytes
        print(f"Sent '{data_to_send}' to Arduino.")
    else:
        print("Can't open serial port.")
    time.sleep(0.5)
    ser.close()
    print("Gracefully exiting the program...")