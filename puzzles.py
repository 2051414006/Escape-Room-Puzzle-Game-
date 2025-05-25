# puzzles.py
# -----------------------------------------------
# Contains logic for all 5 rooms of the GUI Escape Room Game.
# Handles: puzzle questions, answers, hints, and inventory items.
# -----------------------------------------------

import tkinter as tk
from tkinter import messagebox

class PuzzleGame:
    def __init__(self, app):
        self.app = app         # Reference to the main EscapeRoomApp instance
        self.attempts = 0      # Track incorrect attempts per room

    def start_room(self, room_number):
        """
        Starts a new puzzle room based on room_number.
        Resets the attempts counter and loads the corresponding puzzle data.
        """
        self.attempts = 0
        room_data = self.get_room_data(room_number)
        self.display_puzzle(room_data)

    def display_puzzle(self, data):
        """
        Displays the puzzle question in the GUI, handles answer checking,
        provides a hint on the first wrong attempt, and ends game on second.
        """
        frame = self.app.main_frame

        # Puzzle Title
        tk.Label(frame, text=f"🧩 Room {data['room']}", font=("Arial", 14)).pack(pady=10)
        tk.Label(frame, text=data["question"]).pack(pady=5)

        # User Input Box
        entry = tk.Entry(frame)
        entry.pack()

        # Check Button Logic
        def check():
            answer = entry.get().strip().lower()

            if answer == data["answer"].lower():
                messagebox.showinfo("✅ Correct!", "Well done!")

                # If puzzle includes an item (e.g., key), add to inventory
                if data.get("item"):
                    self.app.inventory.append(data["item"])
                    messagebox.showinfo("🗝️ Inventory", f"You found a {data['item']}!")

                self.app.score += 1
                self.app.next_room()
            else:
                self.attempts += 1
                if self.attempts == 1:
                    # Show hint after first wrong attempt
                    messagebox.showwarning("❌ Incorrect", f"Hint: {data['hint']}")
                else:
                    # End game after second wrong attempt
                    messagebox.showerror("💀 Game Over", "Wrong again. You're trapped!")
                    self.app.end_game()

        # Submit Button
        tk.Button(frame, text="Submit", command=check).pack(pady=10)

    def get_room_data(self, index):
        """
        Returns puzzle data (question, answer, hint, optional item)
        based on the current room index (0–4).
        """
        rooms = [
            {
                "room": 1,
                "question": "What has branches but no fruit, trunk or leaves?",
                "answer": "bank",
                "hint": "It's a place, not a plant."
            },
            {
                "room": 2,
                "question": "Next number in the sequence: 2, 4, 8, 16, __?",
                "answer": "32",
                "hint": "Each number doubles."
            },
            {
                "room": 3,
                "question": "Type these colors in reverse: BLUE GREEN RED YELLOW",
                "answer": "yellow red green blue",
                "hint": "Start from the end."
            },
            {
                "room": 4,
                "question": "You found something hanging on a hook. What is it?",
                "answer": "key",
                "hint": "It unlocks things.",
                "item": "key"  # This adds the key to inventory if correct
            },
            {
                "room": 5,
                "question": "Which word doesn’t belong: Apple, Banana, Carrot, Mango?",
                "answer": "carrot",
                "hint": "One is not a fruit."
            }
        ]
        return rooms[index]
