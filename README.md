# Multi-User Project Management Tracking Engine

An elegant, object-oriented Command-Line Interface (CLI) application built in Python to manage and monitor developer profiles, projects, and milestones locally. This system enforces strict relationship constraints, performs contextual input validation, and features rich visual dashboard matrices directly within your console window.

---

## How the Application Works

This application is built on strict Object-Oriented Programming principles, ensuring high data reliability and preventing human entry errors through multiple code layers.

### 1. The Data Objects & Validation Guards
* **Inheritance Layer (`Person` → `User`):** The application utilizes structural inheritance. It sets up a base data class (`Person`) defining foundational characteristics which are automatically passed down and expanded by the operational system identity (`User`).
* **Encapsulation via Properties & Setters:** The internal attributes are heavily protected. Rather than writing raw values directly to code parameters, information passes through validation checkpoints. For instance, trying to assign a blank name or registering an email format missing an `@` symbol will immediately be blocked by the system, raising a managed error.
* **Bounded Work States:** Tasks cannot have random status descriptions. They are constrained strictly to `Pending` or `Completed` statuses via internal code rules.

### 2. Relationship Integrity Constraints
The core engine actively manages data dependencies to prevent broken structural nodes:
* **One-to-Many Relationships:** A `User` can own multiple unique `Projects`, but a `Project` must belong to a valid user. The system blocks the creation of any project unless its declared manager has already been registered in the database.
* **Project-to-Task Linkage:** Tasks are uniquely bound within specific parent Project structures. Case-insensitive mappings ensure that variations in spelling lowercase vs uppercase words do not result in duplicated items.

### 3. State Persistence
The system functions like a lightweight database. When a user creates data via the CLI, an automated serialization pipeline transforms active Python memory objects into organized text entries inside `data/storage.json`. Conversely, whenever a subcommand is initialized, the loading pipeline reads this JSON database, captures integrity faults or file configuration corruptions using robust `try-except` statements, and safely builds the live object states back into memory.

---

## How to Run the Project on Your PC

Follow these straightforward, step-by-step commands to deploy and interact with the software environment locally.

### Step 1: Setting up the project
Fork the repository to your own own github account.
Clone the repository to your own local machine.

### Step 2: Environment Preparation
Open your terminal (Command Prompt, PowerShell) and navigate into your project root directory. First, you need to install the needed dependenecies on your machine, use the given code below

* pip install pipenv
* pipenv install
* pipenv install rich

### Step 3: Running the project
Use **python main.py (command) [options]** to run your commands