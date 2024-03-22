
# import serial
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time


# ser = serial.Serial(
#     port='/dev/ttyACM1',  # Replace with the correct USB port for the Arduino
#     baudrate=115200,
#     timeout=1  # Timeout for read operations, in seconds
# )


def initialize_firebase():
    # Assuming you've already downloaded your Firebase service account key
    cred = credentials.Certificate("intellidesk-174c9-firebase-adminsdk-garkf-abe9a9fb75.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://intellidesk-174c9-default-rtdb.asia-southeast1.firebasedatabase.app/"
    })
    return db.reference()

def send_to_arduino(val):
    data_to_send = f"{val}"

    # Check if serial is open and write data
    # if ser.isOpen():
    #     ser.write(data_to_send.encode())  # Encode string to bytes
    #     print(f"Sent '{data_to_send}' to Arduino.")
    # else:
    #     print("Can't open serial port.")
    pass
# Define a callback function to handle changes in HeightValue
def on_height_value_change(event):
    # This function will be called whenever 'HeightValue' is changed in the database.
    new_value = event.data
    # Do something with the new value
    print(f"HeightValue has changed to: {new_value}")
    send_to_arduino(new_value)

# Initialize the database reference
db = initialize_firebase()

# Now set up a listener on the 'HeightValue' node
height_value_ref = db.child('Controls').child('HeightValue')
height_value_ref.listen(on_height_value_change)

# Keep the script running indefinitely
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Program terminated by user")



