import json
import os
from models.user import User
from models.project import Project

DATA_FILE = os.path.join("data", "storage.json")

def initialize_storage():
    """Ensures directories and data files safely exist."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({"users": [], "projects": []}, f, indent=4)

def load_data():
    """Loads and deserializes JSON data into operational Object lists."""
    initialize_storage()
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            
        users = [User.from_dict(u) for u in data.get("users", [])]
        projects = [Project.from_dict(p) for p in data.get("projects", [])]
        return users, projects
    except (json.JSONDecodeError, KeyError):
        print("[bold red]Error: Local database corrupted. Instantiating fresh runtime environment.[/bold red]")
        return [], []

def save_data(users, projects):
    """Serializes and saves operational Object state back to JSON file."""
    initialize_storage()
    data = {
        "users": [user.to_dict() for user in users],
        "projects": [project.to_dict() for project in projects]
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)