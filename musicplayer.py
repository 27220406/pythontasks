import os
import tkinter as tk
from tkinter import filedialog
from pygame import mixer

# Initialize the mixer
mixer.init()

# Global variables
playlist = []
current_index = 0

# Functions
def load_folder():
    global playlist
    folder = filedialog.askdirectory()
    if folder:
        playlist = [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith(".mp3")]
        if playlist:
            play_song(0)

def play_song(index):
    global current_index
    if playlist:
        current_index = index
        mixer.music.load(playlist[current_index])
        mixer.music.play()
        song_label.config(text=os.path.basename(playlist[current_index]), fg="#FFD700")

def play():
    if not mixer.music.get_busy():
        mixer.music.unpause()
    else:
        play_song(current_index)

def pause():
    mixer.music.pause()

def stop():
    mixer.music.stop()

def next_song():
    global current_index
    if playlist:
        current_index = (current_index + 1) % len(playlist)
        play_song(current_index)

def prev_song():
    global current_index
    if playlist:
        current_index = (current_index - 1) % len(playlist)
        play_song(current_index)

# GUI Setup
root = tk.Tk()
root.title("🎵 Vibrant Music Player")
root.geometry("460x350")
root.configure(bg="#2c3e50")  # dark blue-gray background

# Title Label
title_label = tk.Label(root, text="🎶 My Music Player", font=("Helvetica", 20, "bold"), bg="#2c3e50", fg="#00cec9")
title_label.pack(pady=15)

# Song Label
song_label = tk.Label(root, text="No song playing", font=("Helvetica", 14), bg="#2c3e50", fg="white", wraplength=400)
song_label.pack(pady=10)

# Button Frame
button_frame = tk.Frame(root, bg="#2c3e50")
button_frame.pack(pady=20)

# Style button function
def styled_button(master, text, command):
    return tk.Button(
        master,
        text=text,
        command=command,
        font=("Helvetica", 12, "bold"),
        bg="#00b894",  # greenish
        fg="white",
        activebackground="#55efc4",
        activeforeground="black",
        width=10,
        relief="raised",
        bd=3
    )

# Buttons
styled_button(button_frame, "⏮ Prev", prev_song).grid(row=0, column=0, padx=5, pady=5)
styled_button(button_frame, "▶ Play", play).grid(row=0, column=1, padx=5, pady=5)
styled_button(button_frame, "⏸ Pause", pause).grid(row=0, column=2, padx=5, pady=5)
styled_button(button_frame, "⏹ Stop", stop).grid(row=1, column=0, padx=5, pady=5)
styled_button(button_frame, "⏭ Next", next_song).grid(row=1, column=1, padx=5, pady=5)
styled_button(button_frame, "📁 Load", load_folder).grid(row=1, column=2, padx=5, pady=5)

# Footer
footer = tk.Label(root, text="Powered by tkinter & pygame", font=("Arial", 10), bg="#2c3e50", fg="#7f8c8d")
footer.pack(side="bottom", pady=10)

# Run app
root.mainloop()
