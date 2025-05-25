# main.py
# -----------------------------------------------
# This is the GUI-based version of the Escape Room Puzzle Game.
# It uses tkinter for the interface and logic flow control.
# Includes fixed window size, centering, inventory, and scoring.
# -----------------------------------------------

import tkinter as tk
from tkinter import messagebox
from puzzles import PuzzleGame  # Import puzzle logic from puzzles.py

class EscapeRoomApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Escape Room Puzzle Game")

        # Create an instance of the PuzzleGame logic handler
        self.game = PuzzleGame(self)

        # Main UI frame for all screens
        self.main_frame = tk.Frame(self.root, padx=20, pady=20)
        self.main_frame.pack(expand=True)

        # Initialize game state variables
        self.inventory = []      # Holds found items like 'key'
        self.score = 0           # Tracks number of rooms solved
        self.current_room = 0    # Tracks current room index

        # Start with welcome screen
        self.create_welcome_screen()

    def create_welcome_screen(self):
        """
        Displays the game's introduction screen.
        """
        self.clear_frame()
        tk.Label(self.main_frame, text="🔐 Welcome to the Escape Room!", font=("Arial", 18)).pack(pady=10)
        tk.Label(self.main_frame, text="Solve 5 puzzles to escape.\nWrong once = hint, wrong twice = game over!").pack(pady=5)
        tk.Button(self.main_frame, text="Start Game", command=self.start_game).pack(pady=15)

    def start_game(self):
        """
        Initializes or resets the game and enters the first room.
        """
        self.current_room = 0
        self.score = 0
        self.inventory = []
        self.next_room()

    def next_room(self):
        """
        Moves to the next puzzle room or ends the game if all rooms are done.
        """
        if self.current_room < 5:
            self.clear_frame()
            self.game.start_room(self.current_room)  # Call puzzle logic for the current room
            self.current_room += 1
        else:
            self.final_challenge()

    def final_challenge(self):
        """
        Handles the final stage where the player must enter a passphrase.
        """
        self.clear_frame()
        tk.Label(self.main_frame, text="🔒 Final Lock", font=("Arial", 16)).pack(pady=10)

        # Check if player has found the key
        if "key" not in self.inventory:
            tk.Label(self.main_frame, text="You reached the final door, but you don't have the key!").pack()
            tk.Button(self.main_frame, text="End Game", command=self.end_game).pack(pady=10)
            return

        # If key is present, allow entry of passphrase
        tk.Label(self.main_frame, text="Enter the secret passphrase to escape:").pack()
        entry = tk.Entry(self.main_frame)
        entry.pack()

        def check_pass():
            if entry.get().lower() == "freedom":
                messagebox.showinfo("🎉 Success", "You escaped the room!")
                self.end_game(True)
            else:
                messagebox.showerror("🔒 Locked", "Wrong passphrase. You're still trapped.")
                self.end_game(False)

        tk.Button(self.main_frame, text="Submit", command=check_pass).pack(pady=5)

    def end_game(self, escaped=False):
        """
        Displays the final game result screen.
        """
        self.clear_frame()
        tk.Label(self.main_frame, text=f"Game Over!", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.main_frame, text=f"Score: {self.score} out of 5").pack()

        # Display escape result
        result = "escaped!" if escaped else "got trapped!"
        tk.Label(self.main_frame, text=f"You {result}").pack(pady=5)

        # Option to restart
        tk.Button(self.main_frame, text="Play Again", command=self.start_game).pack(pady=10)

    def clear_frame(self):
        """
        Clears all widgets from the current frame.
        """
        for widget in self.main_frame.winfo_children():
            widget.destroy()

# Main program execution
if __name__ == "__main__":
    root = tk.Tk()

    # Set fixed size and center the window
    window_width = 500
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.resizable(False, False)  # Lock window size

    # Launch the app
    app = EscapeRoomApp(root)
    root.mainloop()
