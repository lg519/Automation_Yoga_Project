import time
import pyautogui
import os
import winsound
from pynput import mouse, keyboard


def beep_prepare():
    frequency = 2000  # Set Frequency To 2500 Hertz
    duration = 1000  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)

def beep_start():
    frequency = 2500  # Set Frequency To 2500 Hertz
    duration = 1000  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)

def beep_end():
    frequency = 500  # Set Frequency To 2500 Hertz
    duration = 1000  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)


def press_button(image_path):
    # find the button on screen
    button_location = pyautogui.locateOnScreen(image_path, confidence=0.8)

    if button_location is not None:
        # get the center of the button
        button_x, button_y = pyautogui.center(button_location)

        # click the button
        pyautogui.click(button_x, button_y)
    else:
        print("Button not found")


def start_exercise():
    beep_prepare()  # Notify the subject to prepare
    time.sleep(1)  # Wait for 2 seconds
    press_button("record_button.JPG")  # Start the recording
    beep_start()  # Notify the subject that the recording has started
    time.sleep(6)
    beep_end()  # Notify the subject that the recording has ended
    press_button("confirm_button.JPG")
    time.sleep(1.5)
    press_button("save_button.JPG")
    


# def on_click(x, y, button, pressed):
#     # If the right button is clicked
#     if button == mouse.Button.right and pressed:
#         start_exercise()


# # Listen for mouse events
# with mouse.Listener(on_click=on_click) as listener:
#     listener.join()


def on_press(key):
    try:
        # If the '#' key is pressed
        if key.char == "#":
            start_exercise()
    except AttributeError:
        pass


# Listen for keyboard events
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
