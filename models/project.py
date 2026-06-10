from typing import List
from models.task import Task

class Project:
    """Represents a Project containing multiple tasks, linked to an owner (User)."""
    def __init__(self, title: str, description: str, due_date: str, owner: str, tasks: List[Task] = None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.owner = owner  # Links to User.name
        self.tasks = tasks if tasks is not None else []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "owner": self.owner,
            "tasks": [task.to_dict() for task in self.tasks]
        }

    @classmethod
    def from_dict(cls, data: dict):
        tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
        return cls(data["title"], data["description"], data["due_date"], data["owner"], tasks)

    def __str__(self) -> str:
        return f"Project: {self.title} | Owner: {self.owner} | Tasks: {len(self.tasks)}"