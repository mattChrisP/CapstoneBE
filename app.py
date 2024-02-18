import time
import cv2
import serial
import random


from detection import ObjectDetection
from camera import BUFFER, get_image
from remap import remap_coor


ins = ObjectDetection()

# For debug purpose only uncomment this one
# cnt = 0

idx = 0

# Need to check and adjust accordingly
CAM1 = "/dev/video0"
CAM2 = "/dev/video1"

ser1 = serial.Serial(
    port='/dev/ttyACM0',  # Replace with the correct USB port for the Arduino
    baudrate=115200,
    timeout=1  # Timeout for read operations, in seconds
)


ser2 = serial.Serial(
    port='/dev/ttyACM1',  # Replace with the correct USB port for the Arduino
    baudrate=115200,
    timeout=1  # Timeout for read operations, in seconds
) 

def neighbor(x,y):
    return [(x+1,y), (x+1, y+1), (x+1, y-1), (x,y), (x,y+1), (x, y-1), (x-1,y+1), (x-1,y), (x-1,y-1)]
time.sleep(2)

cache1 = {}
cache2 = {}

try:
    while True:
        new_cache1 = {}
        new_cache2 = {}
        idx += 1
        if idx == BUFFER + 1:
            idx = 1

        # This is for testing only, remove the cnt for prod
        # if cnt == 5:
        #     break
        st = time.time()

        get_image(CAM1)
        img_path_1 = f"obj{idx}CAM{CAM1}.jpg"

        get_image(CAM2)
        img_path_2 = f"obj{idx}CAM{CAM2}.jpg"


        image_1 = cv2.imread(img_path_1)
        res_1 = ins.detect(img_path_1, idx)

        # Mapping the center of phone coordinate back to image
        print(res_1)

        image_2 = cv2.imread(img_path_2)
        res_2 = ins.detect(img_path_2, idx)

        # Mapping the center of phone coordinate back to image
        print(res_2)

        fin1 = []
        for i in res_1:
            print(i)
            temp = remap_coor(i[0], i[1])

            key = f"{temp[0]},{temp[1]}"
            if key not in cache1:
                # Filter by offset size of box 
                if 17 >= temp[0] >= 1 and 17 >= temp[1] >= 1:
                    fin1.append(temp)

            for i in neighbor(temp[0], temp[1]):
                key = f"{i[0]},{i[1]}"
                new_cache1[key] = 0

        cache1.clear()
        cache1 = new_cache1.copy()
        new_cache1.clear()

        fin2 = []
        for i in res_2:
            print(i)
            temp = remap_coor(i[0], i[1])

            key = f"{temp[0]},{temp[1]}"
            if key not in cache2:
                # Filter by offset size of box 
                if 17 >= temp[0] >= 1 and 17 >= temp[1] >= 1:
                    fin2.append(temp)

            for i in neighbor(temp[0], temp[1]):
                key = f"{i[0]},{i[1]}"
                new_cache2[key] = 0

        cache2.clear()
        cache2 = new_cache2.copy()
        new_cache2.clear()

        print(f"Done in {time.time()-st} s")

        if len(fin1):
            chosen = random.choice(fin1)
            # The string to send to the Arduino
            data_to_send = f"{chosen[0]},{chosen[1]}"

            # Check if serial is open and write data
            if ser1.isOpen():
                ser1.write(data_to_send.encode())  # Encode string to bytes
                print(f"Sent '{data_to_send}' to Arduino.")
            else:
                print("Can't open serial port.")

        if len(fin2):
            chosen = random.choice(fin2)
            # The string to send to the Arduino
            data_to_send = f"{chosen[0]},{chosen[1]}"

            # Check if serial is open and write data
            if ser2.isOpen():
                ser2.write(data_to_send.encode())  # Encode string to bytes
                print(f"Sent '{data_to_send}' to Arduino.")
            else:
                print("Can't open serial port.")
    

        time.sleep(0.5)
        # cnt += 1
except KeyboardInterrupt:
    # Reset to origin
    data_to_send = f"{0},{0}"

    # Check if serial is open and write data
    if ser1.isOpen():
        ser1.write(data_to_send.encode())  # Encode string to bytes
        print(f"Sent '{data_to_send}' to Arduino.")
    else:
        print("Can't open serial port.")

    if ser2.isOpen():
        ser2.write(data_to_send.encode())  # Encode string to bytes
        print(f"Sent '{data_to_send}' to Arduino.")
    else:
        print("Can't open serial port.")
    time.sleep(0.5)
    ser1.close()
    ser2.close()
    print("Gracefully exiting the program...")





