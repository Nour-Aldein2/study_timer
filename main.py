import tkinter as tk
import time
import pygame
import subprocess
from tkinter import ttk
from ttkthemes import ThemedStyle
import sv_ttk



applescript_do_not_disturb = '''
-- Simulate the keyboard shortcut Control+Option+F
tell application "System Events"
    key code 3 using {control down, option down}
end tell
'''
applescript_code = '''
-- Press Command + Space to open the Spotlight search bar
tell application "System Events"
    key code 49 using command down
    delay 1 -- wait for Spotlight to open
end tell

-- Type "Turn On Work Focus"
tell application "System Events"
    keystroke "Work Focus On"
    delay 1 -- wait for search results to appear
end tell

-- Press the down arrow key to select the first search result, then press Enter to activate it
tell application "System Events"
    key code 125 -- down arrow key
    key code 36 -- Enter key
end tell

'''
applescript_code2 = '''
-- Open the search bar
tell application "System Events"
    keystroke space using {command down}
    delay 0.5 -- Wait for the search bar to open
end tell

-- Type the search phrase
tell application "System Events"
    keystroke "Work Focus Off"
    delay 0.5 -- Wait for the search results to appear
end tell

-- Press the down arrow to select the first option
tell application "System Events"
    key code 125 -- down arrow
    delay 0.5 -- Wait for the selection to take effect
    key code 36 -- press return to activate the selection
end tell
'''



class TimerApp:
    def __init__(self, master):
        self.master = master
        master.title("Study Timer")


        # create input fields for hours and minutes
        self.hours_label = ttk.Label(master, text="Hours:")
        self.hours_label.grid(row=0, column=0, padx=(100, 10), pady=(25,0))
        self.hours_entry = tk.Entry(master)
        self.hours_entry.insert(0, "1")
        self.hours_entry.grid(row=0, column=1, pady=(25,0))

        self.minutes_label = ttk.Label(master, text="Minutes:")
        self.minutes_label.grid(row=1, column=0, padx=(100, 10))
        self.minutes_entry = tk.Entry(master)
        self.minutes_entry.insert(0, "0")
        self.minutes_entry.grid(row=1, column=1)

        # create countdown timer display
        self.timer_label = ttk.Label(master, text="00:00:00", font=("Arial", 60))
        self.timer_label.grid(row=2, column=0, columnspan=2, padx=(100, 0))

        # create start/pause button
        self.start_button = ttk.Button(master, text="Start", command=self.start_timer)
        self.start_button.grid(row=3, column=0, pady=(0, 25))

        # create stop button
        self.stop_button = ttk.Button(master, text="Stop", command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.grid(row=3, column=2, padx=(10, 30), pady=(0, 25))

        self.is_running = False
        self.remaining_time = 0
        self.start_time = 0

    def start_timer(self):
        if self.is_running:
            self.pause_timer()
        else:
            # Turn on focus mode
            subprocess.run(['osascript', '-e', applescript_do_not_disturb])

            self.hours_entry.config(state=tk.DISABLED) # disable hours_entry
            self.minutes_entry.config(state=tk.DISABLED) # disable minutes_entry
            hours = int(self.hours_entry.get())
            minutes = int(self.minutes_entry.get())
            self.remaining_time = hours * 3600 + minutes * 60
            self.start_time = time.time()
            self.is_running = True
            self.start_button.config(text="Pause")
            self.stop_button.config(state=tk.NORMAL)
            self.update_timer()
            # Remove label after 13 minutes
            self.master.after(13 * 60 * 1000, self.remove_cool_down_label)

    def remove_cool_down_label(self):
        self.cool_down_label.destroy()

    def pause_timer(self):
        self.is_running = False
        self.start_button.config(text="Resume")
        self.hours_entry.config(state=tk.NORMAL) # enable hours_entry
        self.minutes_entry.config(state=tk.NORMAL) # enable minutes_entry
        # Turn off Do Not Disturb
        subprocess.run(['osascript', '-e', applescript_do_not_disturb])

    def stop_timer(self):
        self.is_running = False
        self.start_button.config(text="Start")
        self.stop_button.config(state=tk.DISABLED)
        self.timer_label.config(text="00:00:00")
        self.hours_entry.config(state=tk.NORMAL) # enable hours_entry
        self.minutes_entry.config(state=tk.NORMAL)  # enable minutes_entry
        # play bell sound using Pygame
        pygame.mixer.init()
        pygame.mixer.music.load("bell.wav")
        pygame.mixer.music.play()
        # Turn off Do Not Disturb
        subprocess.run(['osascript', '-e', applescript_do_not_disturb])
        # Start another timer of 13 minutes
        self.remaining_time = 13 * 60
        self.start_time = time.time()
        self.is_running = True
        self.start_button.config(text="Pause")
        # Add label for "Cooling Down..."
        self.cool_down_label = ttk.Label(self.master, text="Cooling Down ...", font=("Arial", 20))
        self.cool_down_label.grid(row=4, column=0, columnspan=2, pady=20)
        self.update_timer()

    def update_timer(self):
        if self.is_running:
            elapsed_time = time.time() - self.start_time
            time_left = max(self.remaining_time - elapsed_time, 0)
            hours = int(time_left // 3600)
            minutes = int((time_left % 3600) // 60)
            seconds = int(time_left % 60)
            self.timer_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            if time_left == 0:
                self.stop_timer()
            else:
                self.master.after(1000, self.update_timer)


root = tk.Tk()
# This is where the magic happens
sv_ttk.set_theme("dark")

app = TimerApp(root)
root.mainloop()
