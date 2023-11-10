import serial
import time

# Configure the serial connection
ser = serial.Serial(
    port='/dev/ttyUSB0',  # Replace with the correct USB port for the Arduino
    baudrate=9600,
    timeout=1  # Timeout for read operations, in seconds
)

# Wait for the connection to initialize
time.sleep(2)

# The string to send to the Arduino
data_to_send = "40,0"

# Check if serial is open and write data
if ser.isOpen():
    ser.write(data_to_send.encode())  # Encode string to bytes
    print(f"Sent '{data_to_send}' to Arduino.")
else:
    print("Can't open serial port.")

# Give the Arduino time to respond (if needed)
time.sleep(1)

# Close the connection
ser.close()

