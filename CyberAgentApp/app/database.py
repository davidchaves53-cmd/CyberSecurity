import json
import os

DB_FILE = "events.json"

def save_event(event: dict):
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(event)

    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

    return True
