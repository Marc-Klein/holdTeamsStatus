import ctypes
import tkinter as tk
import pyautogui
from threading import Thread, Event
import time


# Constants for SetThreadExecutionState
ES_CONTINUOUS = 0x80000000
ES_DISPLAY_REQUIRED = 0x00000002


def prevent_screen_lock():
    # Set ES_CONTINUOUS combined with ES_DISPLAY_REQUIRED
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_DISPLAY_REQUIRED)


def allow_screen_lock():
    # Clear flags to allow the screen to lock again
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)


def prevent_teams_status(stop_event):
    while not stop_event.is_set():
        pyautogui.press("shift")
        time.sleep(10)


# GUI
def start_prevent():
    prevent_screen_lock()
    start_button["state"] = "disabled"
    stop_button["state"] = "normal"


def stop_prevent():
    allow_screen_lock()
    start_button["state"] = "normal"
    stop_button["state"] = "disabled"


def start_prevent_teams_status():
    global teams_thread, stop_event
    stop_event.clear()
    teams_thread = Thread(target=prevent_teams_status, args=(stop_event,))
    teams_thread.start()
    start_teams_button["state"] = "disabled"
    stop_teams_button["state"] = "normal"


def stop_prevent_teams_status():
    stop_event.set()
    teams_thread.join()
    start_teams_button["state"] = "normal"
    stop_teams_button["state"] = "disabled"


root = tk.Tk()
root.title("")
window_width = 250
window_height = 250
root.minsize(window_width, window_height)
root.maxsize(window_width, window_height)


# prevent_screen_lock gui
start_button = tk.Button(
    root, text="Prevent Screen Lock", command=start_prevent, width=20
)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Allow Screen Lock", command=stop_prevent, width=20)
stop_button.pack(pady=10)
stop_button["state"] = "disabled"

# prevent_teams_status gui
start_teams_button = tk.Button(
    root, text="Prevent Teams Status", command=start_prevent_teams_status, width=20
)
start_teams_button.pack(pady=10)

stop_teams_button = tk.Button(
    root, text="Allow Teams Status", command=stop_prevent_teams_status, width=20
)
stop_teams_button.pack(pady=10)
stop_teams_button["state"] = "disabled"

stop_event = Event()

root.mainloop()
