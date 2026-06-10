from models.person import Person

class User(Person):
    """Represents a User system entity inheriting from Person."""
    def __init__(self, name: str, email: str):
        super().__init__(name, email)

    def to_dict(self) -> dict:
        return {"name": self.name, "email": self.email}

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data["name"], data["email"])

    def __str__(self) -> str:
        return f"User: {self.name} (<{self.email}>)"