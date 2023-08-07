import os
import tkinter as tk
from tkinter.filedialog import askdirectory
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import queue
from tkinter import Tk


class MyHandler(FileSystemEventHandler):
    def __init__(self, src_folder, message_queue):
        self.src_folder = src_folder
        self.message_queue = message_queue

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".otb+"):
            self.update_label()

    def on_deleted(self, event):
        if not event.is_directory and event.src_path.endswith(".otb+"):
            self.update_label()

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith("yoga.txt"):
            self.update_label()

    def update_label(self):
        txt_file = os.path.join(self.src_folder, "yoga.txt")

        with open(txt_file, "r") as f:
            yoga_poses = f.read().splitlines()

        otb_plus_files = [
            f
            for f in os.listdir(self.src_folder)
            if os.path.isfile(os.path.join(self.src_folder, f)) and f.endswith(".otb+")
        ]
        otb_plus_count = len(otb_plus_files)

        if otb_plus_count == 0 and len(yoga_poses) > 0:
            message = f"Next 1: {yoga_poses[0]}"
        elif otb_plus_count < len(yoga_poses):
            message = f"Next {otb_plus_count + 1}: {yoga_poses[otb_plus_count]}"
        else:
            message = "No poses left"

        self.message_queue.put(message)


def watch_folder():
    Tk().withdraw()

    src_folder = askdirectory(title="Select the Folder with .otb+ files")

    window = tk.Tk()
    window.title("Yoga Pose Monitor")
    window.attributes("-topmost", 1)
    window.geometry("900x80")  # Resized the window to 300x30
    label = tk.Label(window, text="", font=("Helvetica", 64))  # Set the font size to 16
    label.pack()
    window.update()

    message_queue = queue.Queue()

    event_handler = MyHandler(src_folder, message_queue)
    observer = Observer()
    observer.schedule(event_handler, path=src_folder, recursive=False)
    observer.start()

    # Added this block to handle the case where no .otb+ files are present initially
    event_handler.update_label()

    def update_label():
        try:
            message = message_queue.get_nowait()
        except queue.Empty:
            pass
        else:
            label["text"] = message
            window.update()

        window.after(100, update_label)

    window.after(100, update_label)

    try:
        window.mainloop()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    watch_folder()
