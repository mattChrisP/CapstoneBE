# This is controller.py
import subprocess
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


wireless_charger_status = False
processes = []


def initialize_firebase():
    # Assuming you've already downloaded your Firebase service account key
    cred = credentials.Certificate("intellidesk-174c9-firebase-adminsdk-garkf-abe9a9fb75.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://intellidesk-174c9-default-rtdb.asia-southeast1.firebasedatabase.app/"
    })
    return db.reference()


def on_wireless_charger_status_change(event):
    global wireless_charger_status
    wireless_charger_status = True if event.data else False
    if wireless_charger_status:
        run_scripts()
    else:
        terminate_scripts()
    print(f"WirelessCharging status has changed to: {wireless_charger_status}")


def run_scripts():
    global processes
    ## List of paths to the worker scripts
    worker_scripts = ['app1.py', 'app2.py']
    # List to keep track of the subprocesses for each worker script
    

    # Start all the worker scripts
    for script in worker_scripts:
        print(f"Starting {script}")
        process = subprocess.Popen(['python', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        processes.append(process)


def terminate_scripts():
    global processes

    # Terminate all the worker scripts
    for process in processes:
        print("Terminating a worker script")
        process.terminate()

    # Wait for all the worker scripts to terminate and print their output
    for process in processes:
        process.wait()  # Wait for the process to terminate
        output, errors = process.communicate()  # Get the output and errors
        if output:
            print("Worker output:", output.decode())
        if errors:
            print("Worker errors:", errors.decode())

    processes = []
    

# Initialize the database reference
db = initialize_firebase()

# Setting up the listener
wireless_charging_ref = db.child('Controls').child('ChargingCamera')
wireless_charging_ref.listen(on_wireless_charger_status_change) 


# Keep the script running indefinitely
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Program terminated by user")
