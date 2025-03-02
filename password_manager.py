from tkinter import *
from tkinter import messagebox
import random
import json
import pyperclip
from cryptography.fernet import Fernet
import customtkinter as ctk

# Generate encryption key (Save this key securely)
KEY = Fernet.generate_key()
cipher = Fernet(KEY)

# Theme Colors
BG_COLOR = "#FFFFFF"  # White background
TEXT_COLOR = "#000000"  # Black text
BUTTON_COLOR = "#3A86FF"  # Blue Buttons
FONT = ("Poppins", 14, "bold")
ENTRY_BG = "#F0F0F0"
ENTRY_FG = "#000000"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    symbols = '!#$%&()*+'
    
    password_list = (
        random.choices(letters, k=random.randint(8, 10)) +
        random.choices(symbols, k=random.randint(2, 4)) +
        random.choices(numbers, k=random.randint(2, 4))
    )
    random.shuffle(password_list)
    password = "".join(password_list)
    pyperclip.copy(password)
    password_input.delete(0, END)
    password_input.insert(0, password)
    return password

# ---------------------------- SAVE PASSWORD ------------------------------- #
def encrypt_data(data):
    """Encrypts data using AES encryption."""
    return cipher.encrypt(data.encode()).decode()

def save_password():
    website = website_input.get().strip()
    username = username_input.get().strip()
    password = password_input.get().strip()
    
    if not website or not username or not password:
        messagebox.showerror("Error", "No empty fields allowed!")
        return
    
    encrypted_password = encrypt_data(password)
    new_data = {website: {"username": username, "password": encrypted_password}}
    
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    
    data.update(new_data)
    
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)
    
    website_input.delete(0, END)
    username_input.delete(0, END)
    password_input.delete(0, END)
    messagebox.showinfo("Success", "Password saved successfully!")

# ---------------------------- UI SETUP ------------------------------- #
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

window = ctk.CTk()
window.title("Secure Password Manager")
window.geometry("500x550")
window.configure(bg=BG_COLOR)

frame = ctk.CTkFrame(window, corner_radius=15, fg_color=BG_COLOR)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Image (Full Size)
canvas = Canvas(frame, width=480, height=200, bg=BG_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2, pady=10)
mypass_img = PhotoImage(file="logo.png")  # Ensure this image exists
canvas.create_image(240, 100, image=mypass_img)  # Centered image

# Labels and Inputs in Grid Layout
website_label = ctk.CTkLabel(frame, text="Website:", font=FONT, text_color=TEXT_COLOR)
website_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

website_input = ctk.CTkEntry(frame, width=250, height=40, corner_radius=10, fg_color=ENTRY_BG, text_color=ENTRY_FG)
website_input.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

username_label = ctk.CTkLabel(frame, text="Email/Username:", font=FONT, text_color=TEXT_COLOR)
username_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

username_input = ctk.CTkEntry(frame, width=250, height=40, corner_radius=10, fg_color=ENTRY_BG, text_color=ENTRY_FG)
username_input.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

password_label = ctk.CTkLabel(frame, text="Password:", font=FONT, text_color=TEXT_COLOR)
password_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

password_input = ctk.CTkEntry(frame, width=250, height=40, corner_radius=10, fg_color=ENTRY_BG, text_color=ENTRY_FG, show="*")
password_input.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

# Buttons
gen_pass_button = ctk.CTkButton(frame, text="Generate Password", fg_color=BUTTON_COLOR, corner_radius=10, text_color="white", command=generate_password)
gen_pass_button.grid(row=4, column=0, columnspan=2, pady=10)

add_button = ctk.CTkButton(frame, text="Add", fg_color=BUTTON_COLOR, corner_radius=10, text_color="white", command=save_password)
add_button.grid(row=5, column=0, columnspan=2, pady=10)

window.mainloop()

