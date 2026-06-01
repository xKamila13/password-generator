import json
import os
from datetime import datetime

MAX_HISTORY = 15 
HISTORY_FILE = "history.json"

_history = []


def _load():

    global _history
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            _history = json.load(f)
    else:
        _history = []


def _save():

    with open(HISTORY_FILE, "w") as f:
        json.dump(_history, f, indent=2)


def add_to_history(password, hard):

    entry = {
        "password": password,
        "type":     "Hard" if hard else "Easy",
        #"time":     datetime.now().strftime("%H:%M:%S")
    }
    _history.insert(0, entry)


    if len(_history) > MAX_HISTORY:
        _history.pop()

    _save()


def get_history():
    return _history[:]


def clear_history():
    _history.clear()
    _save()



_load()