import tkinter as tk
from tkinter import filedialog, messagebox
from pygame import mixer
from pygame.locals import *
import os

# Initialize the mixer
mixer.init()

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Music Player")
        self.root.geometry("500x300")

        # Initialize player variables
        self.current_track = ""
        
        # Create and place widgets
        self.load_button = tk.Button(root, text="Load", command=self.load_music)
        self.load_button.pack(pady=10)
        
        self.play_button = tk.Button(root, text="Play", command=self.play_music)
        self.play_button.pack(pady=10)
        
        self.pause_button = tk.Button(root, text="Pause", command=self.pause_music)
        self.pause_button.pack(pady=10)
        
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_music)
        self.stop_button.pack(pady=10)

        self.volume_label = tk.Label(root, text="Volume")
        self.volume_label.pack(pady=5)
        
        self.volume_scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_volume)
        self.volume_scale.set(50)  # Set default volume
        self.volume_scale.pack(pady=10)
        
        self.progress_label = tk.Label(root, text="Playback Position")
        self.progress_label.pack(pady=5)
        
        self.progress_scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_position)
        self.progress_scale.pack(pady=10)
        
        self.status_label = tk.Label(root, text="")
        self.status_label.pack(pady=10)

        self.paused = False
        
    def load_music(self):
        self.current_track = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3")])
        if self.current_track:
            self.status_label.config(text=f"Loaded: {os.path.basename(self.current_track)}")
        else:
            self.status_label.config(text="No track loaded")

    def play_music(self):
        if self.current_track:
            mixer.music.load(self.current_track)
            mixer.music.play()
            self.paused = False
            self.update_progress()
        else:
            messagebox.showwarning("Warning", "No track loaded")

    def pause_music(self):
        if self.current_track:
            if not self.paused:
                mixer.music.pause()
                self.paused = True
                self.status_label.config(text="Paused")
            else:
                mixer.music.unpause()
                self.paused = False
                self.status_label.config(text="Playing")
        else:
            messagebox.showwarning("Warning", "No track loaded")

    def stop_music(self):
        mixer.music.stop()
        self.status_label.config(text="Stopped")
        self.progress_scale.set(0)

    def set_volume(self, val):
        volume = int(val) / 100
        mixer.music.set_volume(volume)

    def set_position(self, val):
        if mixer.music.get_busy():
            mixer.music.play(loops=0, start=int(val))

    def update_progress(self):
        if mixer.music.get_busy():
            self.root.after(1000, self.update_progress)  
            
root = tk.Tk()
player = MusicPlayer(root)
root.mainloop()
