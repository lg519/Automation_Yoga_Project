import subprocess
import atexit
import keyboard

# Start the subprocesses
proc1 = subprocess.Popen(["python", "beep_recording.py"])
proc2 = subprocess.Popen(["python", "print_yoga_pose_name.py"])


# Define a function to terminate the subprocesses
def cleanup():
    proc1.terminate()
    proc2.terminate()


# Register the cleanup function to be called on exit
atexit.register(cleanup)

print("Press Esc to exit...")

# Wait for Esc key to be pressed
keyboard.wait("esc")
