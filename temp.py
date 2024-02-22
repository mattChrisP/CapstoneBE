import serial
import time
ser = serial.Serial(
    port='/dev/ttyACM1',  # Replace with the correct USB port for the Arduino
    baudrate=115200,
    timeout=1  # Timeout for read operations, in seconds
)
time.sleep(2)

data_to_send = f"3,5"

# Check if serial is open and write data
if ser.isOpen():
    ser.write(data_to_send.encode())  # Encode string to bytes
    print(f"Sent '{data_to_send}' to Arduino.")
    

    ser.close()
else:
    print("Can't open serial port.")