import unittest
from models.user import User
from models.project import Project
from models.task import Task

class TestProjectTracker(unittest.TestCase):

    def test_user_creation_and_properties(self):
        user = User("Alice Smith", "alice@example.com")
        self.assertEqual(user.name, "Alice Smith")
        self.assertEqual(user.email, "alice@example.com")
        
        # Test Validation Error Logic Bounds
        with self.assertRaises(ValueError):
            user.email = "bad_email_format"

    def test_project_task_aggregation(self):
        project = Project("Backend Setup", "Build core engine", "2026-12-31", "Alice Smith")
        task = Task("Configure DB Configuration")
        
        project.add_task(task)
        self.assertEqual(len(project.tasks), 1)
        self.assertEqual(project.tasks[0].title, "Configure DB Configuration")
        self.assertEqual(project.tasks[0].status, "Pending")

    def test_task_status_mutator_validation(self):
        task = Task("Write Documentation")
        task.status = "Completed"
        self.assertEqual(task.status, "Completed")
        
        with self.assertRaises(ValueError):
            task.status = "Invalid Status Mode Flag"

if __name__ == "__main__":
    unittest.main()