import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os
import pygame  # Import pygame for music playback

# Check environment for tkinter support
try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError as e:
    raise EnvironmentError("Tkinter module is not available in this environment. Please ensure Tkinter is installed and supported.")

# Initialize pygame mixer for background music
pygame.mixer.init()

# Load and play background music
music_file = os.path.join(os.getcwd(), "media", "music.mp3")
try:
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(-1)  # Play the music on a loop
except Exception as e:
    print(f"Error loading or playing music: {e}")

# Create the main window
root = tk.Tk()
root.title("Spidey and His Amazing Friends Memory Game")
root.geometry("900x700")  # Set window size

# Path to the media folder
media_folder = os.path.join(os.getcwd(), "media")

# Characters and their images
characters = [
    "Spidey.png", "Spin.png", "Ghosty.png", "Black Panther.png",
    "Iron Man.png", "Green Goblin.png", "Doc Ock.png", "Rhino.png", "Black Cat.png"
]

# Duplicate the character list for matching pairs
character_pairs = characters * 2

# Shuffle the cards
random.shuffle(character_pairs)

# Keep track of game state
flipped_cards = []  # Indices of flipped cards
matched_cards = []  # Indices of matched cards
buttons = []  # List of button widgets
images = {}  # Dictionary to store loaded images

# Placeholder image for unmatched cards
try:
    default_image = ImageTk.PhotoImage(Image.new("RGBA", (100, 100), "gray"))
except Exception as e:
    print(f"Error creating placeholder image: {e}")
    default_image = None

# Load images for the characters
for character in characters:
    image_path = os.path.join(media_folder, character)
    try:
        pil_image = Image.open(image_path).resize((100, 100))  # Resize to fit button size
        images[character] = ImageTk.PhotoImage(pil_image)
    except Exception as e:
        print(f"Error loading {character}: {e}")
        images[character] = default_image  # Use placeholder if loading fails

# Callback for card flip
def flip_card(index):
    global flipped_cards

    # Ignore clicks on already matched or currently flipped cards
    if index in matched_cards or len(flipped_cards) == 2 or index in flipped_cards:
        return

    # Flip the card (show the character image)
    buttons[index].config(image=images[character_pairs[index]], state="disabled")
    flipped_cards.append(index)

    # Check for a match if two cards are flipped
    if len(flipped_cards) == 2:
        root.after(1000, check_match)

# Check if the flipped cards match
def check_match():
    global flipped_cards, matched_cards

    index1, index2 = flipped_cards
    if character_pairs[index1] == character_pairs[index2]:
        # Mark as matched
        matched_cards.extend([index1, index2])
        buttons[index1].config(bg="#98FB98", state="disabled")  # Green for matched cards
        buttons[index2].config(bg="#98FB98", state="disabled")
    else:
        # Reset unmatched cards
        buttons[index1].config(image=default_image, state="normal")
        buttons[index2].config(image=default_image, state="normal")

    flipped_cards = []

    # Check if the game is won
    if len(matched_cards) == len(character_pairs):
        messagebox.showinfo("Congratulations!", "You've matched all the cards!")
        reset_game()

# Reset the game board
def reset_game():
    global flipped_cards, matched_cards, buttons

    flipped_cards = []
    matched_cards = []

    # Reset buttons and reshuffle cards
    random.shuffle(character_pairs)
    for i, button in enumerate(buttons):
        button.config(image=default_image, bg="#f0f0f0", state="normal")

# Create the game board
def create_board():
    global buttons

    # Title Label
    title_label = tk.Label(root, text="Spidey and His Amazing Friends Memory Game", font=("Arial", 20, "bold"), bg="#282c34", fg="white")
    title_label.pack(pady=20)

    # Frame for the game board
    frame = tk.Frame(root, bg="#282c34")
    frame.pack()

    # Create a 6x3 grid of buttons
    for i in range(6):
        for j in range(3):
            index = i * 3 + j
            button = tk.Button(frame, text="", width=110, height=110, image=default_image, command=lambda idx=index: flip_card(idx))
            button.grid(row=i, column=j, padx=10, pady=10)
            buttons.append(button)

def start_game():
    menu_frame.pack_forget()
    create_board()

# Create the start menu
def create_start_menu():
    global menu_frame

    menu_frame = tk.Frame(root, bg="#282c34")
    menu_frame.pack(fill="both", expand=True)

    # Background image for the menu
    menu_image_path = os.path.join(media_folder, "menu.png")
    try:
        menu_image = ImageTk.PhotoImage(Image.open(menu_image_path).resize((900, 700)))
        menu_label = tk.Label(menu_frame, image=menu_image)
        menu_label.image = menu_image  # Keep a reference to avoid garbage collection
        menu_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"Error loading menu background image: {e}")

    # Play button using an image
    play_button_image_path = os.path.join(media_folder, "play.png")
    try:
        play_button_image = ImageTk.PhotoImage(Image.open(play_button_image_path).resize((150, 50)))
        play_button = tk.Button(menu_frame, image=play_button_image, command=start_game, bg="#282c34", borderwidth=0)
        play_button.image = play_button_image  # Keep a reference to avoid garbage collection
        play_button.place(relx=0.5, rely=0.85, anchor="center")
    except Exception as e:
        print(f"Error loading play button image: {e}")

create_start_menu()

# Run the main event loop
root.mainloop()
