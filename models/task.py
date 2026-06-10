class Task:
    """Represents a Task within a project."""
    def __init__(self, title: str, assigned_to: str = "Unassigned", status: str = "Pending"):
        self.title = title
        self.assigned_to = assigned_to
        self._status = status

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        valid_statuses = ["Pending", "In Progress", "Completed"]
        if value not in valid_statuses:
            raise ValueError(f"Status must be one of {valid_statuses}")
        self._status = value

    def to_dict(self) -> dict:
        return {"title": self.title, "assigned_to": self.assigned_to, "status": self.status}

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data["title"], data["assigned_to"], data["status"])

    def __str__(self) -> str:
        return f"[{self.status}] {self.title} (Assigned to: {self.assigned_to})"