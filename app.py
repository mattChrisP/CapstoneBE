import time
import cv2
import serial


from detection import ObjectDetection
from camera import BUFFER, get_image
from remap import remap_coor


ins = ObjectDetection()

# For debug purpose only uncomment this one
# cnt = 0

idx = 0

ser = serial.Serial(
    port='/dev/ttyUSB0',  # Replace with the correct USB port for the Arduino
    baudrate=9600,
    timeout=1  # Timeout for read operations, in seconds
)

time.sleep(2)

try:
    while True:
        idx += 1
        if idx == BUFFER + 1:
            idx = 1

        # This is for testing only, remove the cnt for prod
        # if cnt == 5:
        #     break
        st = time.time()
        get_image()
        img_path = f"obj{idx}.jpg"
        image = cv2.imread(img_path)

        res = ins.detect(img_path, idx)


        # Mapping the center of phone coordinate back to image
        print(res)
        fin = [0, 0]
        for i in res:
            print(i)
            fin = remap_coor(i[0], i[1])
        print(f"Done in {time.time()-st} s")

        # The string to send to the Arduino
        data_to_send = f"{fin[0]},{fin[1]}"

        # Check if serial is open and write data
        if ser.isOpen():
            ser.write(data_to_send.encode())  # Encode string to bytes
            print(f"Sent '{data_to_send}' to Arduino.")
        else:
            print("Can't open serial port.")

        time.sleep(0.5)
        # cnt += 1
except KeyboardInterrupt:
    ser.close()
    print("Gracefully exiting the program...")


