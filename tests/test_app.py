"""Small built-in unittest suite: no extra test package required."""

import unittest

from app import app, tasks


class TaskFlowTests(unittest.TestCase):
    def setUp(self):
        tasks.clear()
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "ok"})

    def test_add_and_delete_via_forms(self):
        self.assertIn(b"No tasks yet", self.client.get("/").data)
        response = self.client.post("/add", data={"task": "Learn Flask"}, follow_redirects=True)
        self.assertIn(b"Learn Flask", response.data)
        self.assertEqual(tasks, ["Learn Flask"])
        response = self.client.post("/delete/0", follow_redirects=True)
        self.assertIn(b"No tasks yet", response.data)
        self.assertEqual(tasks, [])

    def test_blank_task_is_ignored(self):
        self.client.post("/add", data={"task": "   "})
        self.assertEqual(tasks, [])

    def test_out_of_range_delete_is_safe(self):
        self.client.post("/delete/999")
        self.assertEqual(tasks, [])


if __name__ == "__main__":
    unittest.main()
