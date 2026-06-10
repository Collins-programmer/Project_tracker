class Person:
    """Base class to represent a person, showcasing inheritance."""
    def __init__(self, name: str, email: str):
        self._name = name
        self._email = email

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        self._name = value

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        if "@" not in value:
            raise ValueError("Invalid email address format.")
        self._email = value