# 🔐 Password Generator

A simple and clean password generator desktop app built with Python and CustomTkinter.

## Screenshot

<img width="784" height="1172" alt="image" src="https://github.com/user-attachments/assets/55fb36ff-cc4f-4a32-929f-b31af324cd90" />


## Features

- Adjustable password length (7–20 characters)
- Two difficulty modes:
  - **Easy** – letters + digits
  - **Hard** – letters + digits + special characters (`!@#$%^&*_+-=?`)
- Password strength indicator
- One-click copy to clipboard
- History of last 15 generated passwords (saved between sessions)

## Requirements

- Python 3.8+
- CustomTkinter 5.2.2

## Installation

Clone or download the repository, then install dependencies:

pip install customtkinter


## Usage

python main.py


## Project Structure

| File | Description |
|---|---|
| `main.py` | GUI – main application window |
| `generator.py` | Password generation logic |
| `history_manager.py` | History management and file saving |
| `requirements.txt` | List of dependencies |
