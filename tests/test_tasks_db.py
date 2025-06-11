import unittest
import os
import sqlite3
from logic import tasks_db

class TestTasksDB(unittest.TestCase):
    TEST_DB = "test_tasks.db"

    def setUp(self):
        # Testdatenbank anlegen
        tasks_db.DB_PATH = self.TEST_DB
        tasks_db.init_db()

    def tearDown(self):
        # Testdatenbank löschen
        if os.path.exists(self.TEST_DB):
            os.remove(self.TEST_DB)

    def test_add_and_get_task(self):
        tasks_db.add_task("Testaufgabe", status="To Do")
        tasks = tasks_db.get_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0][1], "Testaufgabe")
        self.assertEqual(tasks[0][2], "To Do")

    def test_update_task_status(self):
        tasks_db.add_task("Statusaufgabe", status="To Do")
        task_id = tasks_db.get_tasks()[0][0]
        tasks_db.update_task_status(task_id, "Done")
        updated = tasks_db.get_tasks()[0]
        self.assertEqual(updated[2], "Done")

    def test_delete_task(self):
        tasks_db.add_task("Löschen", status="To Do")
        task_id = tasks_db.get_tasks()[0][0]
        tasks_db.delete_task(task_id)
        self.assertEqual(len(tasks_db.get_tasks()), 0)

if __name__ == "__main__":
    unittest.main()