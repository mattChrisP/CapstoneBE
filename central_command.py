# This is controller.py
import subprocess
import time
import threading
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


def handle_process_output(process, script_name):
    """Handle all output (standard output and standard error) of each script in real-time."""
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(f"{script_name}: {output.strip()}")
    process.stdout.close()

def run_scripts():
    global processes
    worker_scripts = ['app1.py', 'app2.py']
    for script in worker_scripts:
        print(f"Starting {script}")
        # Note the stderr=subprocess.STDOUT here
        process = subprocess.Popen(['python', script], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, text=True)
        processes.append(process)
        
        # Start a thread for handling the combined output and errors
        output_thread = threading.Thread(target=handle_process_output, args=(process, script))
        output_thread.start()


def terminate_scripts():
    global processes
    for process in processes:
        print("Terminating a worker script")
        process.terminate()

    # # Now wait for all scripts to terminate after issuing the terminate command
    # for process in processes:
    #     process.wait()  # Wait for the process to terminate
    #     output, errors = process.communicate()  # Collect final output and errors if any
    #     if output:
    #         print("Worker output:", output)
    #     if errors:
    #         print("Worker errors:", errors)

    processes = []  # Clear the list of processes after all have been terminated


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
