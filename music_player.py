import tkinter as tk
import pygame
import os
import random
import threading

class MusicPlayer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Music Player")
        self.geometry("1280x720")
        # Load the image for the background
        image_path = "background.png"
        self.background_image = tk.PhotoImage(file=image_path)

        # Set the background image of the main window (root)
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.song_list = []  # List to store the song file names
        self.matched_song_indices = []  # List to store indices of matched songs
        self.shuffle_song_indices = []  # List to store indices of matched songs
        self.current_song_index = 0

        # Initialize Pygame video system (even if not used)
        pygame.init()
        # Initialize Pygame mixer
        pygame.mixer.init()

        # Set the end event to a custom event number (e.g., 25)
        pygame.mixer.music.set_endevent(25)

        # Call functions to create the GUI and load songs
        self.create_gui()
        self.load_songs()

        # Start the event loop to check for the end event
        self.check_end_event()


    def create_gui(self):
        # Add GUI elements (buttons, listbox, etc.)
        self.skip_button = tk.Button(self, bg="lightgray", text="Skip", command=self.skip_song_button,font=("Times new roman",10), width=10, height=2)
        self.skip_button.grid(row=1, column=4, padx=10, pady=200)

        self.pause_button = tk.Button(self, bg="lightgray", text="Pause", command=self.pause_song,font=("Times new roman",10), width=10, height=2)
        self.pause_button.grid(row=1, column=5, padx=10, pady=200)

        self.play_button = tk.Button(self, bg="lightgray", text="Play", command=self.play_song, font=("Times new roman",10), width=10, height=2)
        self.play_button.grid(row=1, column=6, padx=10, pady=200)

        self.resume_button = tk.Button(self, bg="lightgray", text="Resume", command=self.resume_song,font=("Times new roman",10), width=10, height=2)
        self.resume_button.grid(row=1, column=7, padx=10, pady=200)

        self.shuffle_button = tk.Button(self, bg="lightgray", text="Shuffle", command=self.shuffle_list,font=("Times new roman",10), width=10, height=2)
        self.shuffle_button.grid(row=1, column=8, padx=10, pady=200)

        self.song_listbox = tk.Listbox(self, bg="lightgray", fg="black",font=("Times new roman",10), width=100, height=10)
        self.song_listbox.grid(row=1, column=1, columnspan=3, padx=30, pady=50)

        # Add the search entry and button
        self.search_entry = tk.Entry(self, font=("Times new roman", 12), width=30)
        self.search_entry.grid(row=2, column=1, padx=5, pady=10)
        
        self.search_button = tk.Button(self, text="Search", command=self.search_songs, font=("Times new roman", 10), width=10, height=1)
        self.search_button.grid(row=2, column=2, padx=5, pady=10)

        # Add songs to the listbox
        for song in self.song_list:
            self.song_listbox.insert(tk.END, song)

        # Bind double click on a song to play it
        self.song_listbox.bind("<Double-Button-1>", self.play_selected_song)


    def load_songs(self):
        # Load song files from the music folder and add them to the song_list
        music_folder = "Music Folder"
        for filename in os.listdir(music_folder):
            if filename.endswith(".mp3"):  # Change the file extension as needed
                self.song_list.append(filename)
        for song in self.song_list:
            self.song_listbox.insert(tk.END, song)

    def play_song(self):
        # Play the current song
        current_song = os.path.join("Music Folder", self.song_list[self.current_song_index])
        pygame.mixer.music.load(current_song)
        pygame.mixer.music.play()

    def play_next(self):
        # Code to play next song
        self.current_song_index += 1
        if self.current_song_index >= len(self.song_list):
            self.current_song_index = 0
        next_song = os.path.join("Music Folder", self.song_list[self.current_song_index])
        pygame.mixer.music.load(next_song)
        pygame.mixer.music.play()

    def resume_song(self):
        # Resume the paused song
        pygame.mixer.music.unpause()

    def pause_song(self):
        # Pause the currently playing song
        pygame.mixer.music.pause()

    def skip_song(self):
        # Skip to the next song in the playlist
        pygame.mixer.music.stop()
        self.current_song_index = (self.current_song_index + 1) % len(self.song_list)
        self.play_song()

    def skip_song_button(self):
        # Skip to the next song in the playlist
        pygame.mixer.music.stop()
        self.check_end_event

    def play_selected_song(self, event):
        selected_song_index = self.song_listbox.curselection()
        if selected_song_index:
            selected_index = selected_song_index[0]
            if self.matched_song_indices:
                selected_index = self.matched_song_indices[selected_index]
            if self.shuffle_song_indices:
                selected_index=self.shuffle_song_indices[selected_index]
            self.current_song_index = selected_index
            self.play_song()

    def shuffle_list(self):
        self.matched_song_indices=[]
        self.shuffle_song_indices=[]
        random.shuffle(self.song_list)
        self.shuffle_song_indices=[index for index, song in enumerate(self.song_list)]
        self.song_listbox.delete(0, tk.END)
        for index in self.shuffle_song_indices:
            self.song_listbox.insert(tk.END, self.song_list[index])

    def search_songs(self):

        # Get the search term from the entry widget
        self.matched_song_indices=[]
        self.shuffle_song_indices=[]
        search_term = self.search_entry.get().lower()
        # Filter the song list to show only the matching songs
        self.matched_song_indices = [
            index for index, song in enumerate(self.song_list) if search_term in song.lower()
        ]
        self.song_listbox.delete(0, tk.END)
        for index in self.matched_song_indices:
            self.song_listbox.insert(tk.END, self.song_list[index])

    def check_end_event(self):
        # Function to check for the end event (music has ended)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == 25:  # Custom event number for music end
                self.skip_song()
        # Schedule the check_end_event function to be called again after 100 milliseconds
        self.after(100, self.check_end_event)

if __name__ == "__main__":
    app = MusicPlayer()
    app.mainloop()