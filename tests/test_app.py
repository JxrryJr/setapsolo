"""Automated equivalence-partition tests for Supervisor Finder."""

import os
import tempfile
import unittest

from app import create_app, validate_interest, validate_profile


class SupervisorFinderTests(unittest.TestCase):
    def setUp(self):
        handle, self.database = tempfile.mkstemp()
        os.close(handle)
        self.app = create_app({"TESTING": True, "DATABASE": self.database, "SECRET_KEY": "test"})
        self.client = self.app.test_client()

    def tearDown(self):
        os.unlink(self.database)

    def login(self, email="ada@university.ac.uk", password="demo123"):
        return self.client.post("/login", data={"email": email, "password": password}, follow_redirects=True)

    # Directory/search partitions: no query, matching query, no-match query.
    def test_directory_lists_staff_and_filters_by_interest(self):
        response = self.client.get("/staff")
        self.assertIn(b"3 supervisors found", response.data)
        response = self.client.get("/staff?interest=Graph+theory")
        self.assertIn(b"Dr James Okafor", response.data)
        self.assertNotIn(b"Dr Ada Bennett", response.data)

    def test_directory_no_match_has_clear_empty_state(self):
        response = self.client.get("/staff?q=unfindable-subject")
        self.assertIn(b"No supervisors matched", response.data)

    # Authentication partitions: valid credentials, wrong password, missing protected session.
    def test_valid_login_reaches_dashboard(self):
        response = self.login()
        self.assertIn(b"Hello, Dr Ada Bennett", response.data)

    def test_invalid_login_is_rejected(self):
        response = self.client.post("/login", data={"email": "ada@university.ac.uk", "password": "wrong"})
        self.assertIn(b"Email or password was not recognised", response.data)

    def test_dashboard_requires_authentication(self):
        response = self.client.get("/dashboard", follow_redirects=True)
        self.assertIn(b"Please sign in as a staff member", response.data)

    # Interest partitions: boundary-invalid, valid, duplicate and ownership failure.
    def test_interest_validation_boundaries(self):
        self.assertIsNotNone(validate_interest("A"))
        self.assertIsNone(validate_interest("AI"))
        self.assertIsNotNone(validate_interest("x" * 61))

    def test_add_and_reject_duplicate_interest(self):
        self.login()
        response = self.client.post("/dashboard/interests", data={"name": "Software testing"}, follow_redirects=True)
        self.assertIn(b"Area of interest added", response.data)
        response = self.client.post("/dashboard/interests", data={"name": "software testing"}, follow_redirects=True)
        self.assertIn(b"already on your profile", response.data)

    # Project creation partitions: correctly populated valid record and missing-title invalid record.
    def valid_project(self):
        return {"title": "Testing accessible study tools", "summary": "Develop and evaluate a simple tool that helps students plan focused study sessions using accessible interaction patterns.", "skills": "Python, accessibility", "project_type": "Development", "availability": "Available"}

    def test_create_project_with_valid_data(self):
        self.login()
        response = self.client.post("/dashboard/projects/new", data=self.valid_project(), follow_redirects=True)
        self.assertIn(b"Project idea published", response.data)
        self.assertIn(b"Testing accessible study tools", response.data)

    def test_project_with_missing_title_is_not_saved(self):
        self.login()
        project = self.valid_project()
        project["title"] = ""
        response = self.client.post("/dashboard/projects/new", data=project, follow_redirects=True)
        self.assertIn(b"Title must contain between 5 and 120 characters", response.data)
        self.assertNotIn(b"Project idea published", response.data)

    def test_staff_cannot_edit_another_staff_project(self):
        self.login()
        response = self.client.get("/dashboard/projects/3/edit")
        self.assertEqual(response.status_code, 403)
        self.assertIn(b"do not have permission", response.data)

    # Profile boundaries: minimum/maximum invalid partitions and normal valid partition.
    def test_profile_validation_partitions(self):
        self.assertEqual(len(validate_profile("CS", "A" * 30)), 0)
        self.assertEqual(len(validate_profile("C", "A" * 29)), 2)
        self.assertEqual(len(validate_profile("C" * 101, "A" * 1001)), 2)

    def test_save_project_toggles_session_list(self):
        response = self.client.post("/projects/1/save", follow_redirects=True)
        self.assertIn(b"Project saved for this browsing session", response.data)
        response = self.client.post("/projects/1/save", follow_redirects=True)
        self.assertIn(b"Project removed from your saved list", response.data)


if __name__ == "__main__":
    unittest.main()
