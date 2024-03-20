import json
import os
import unittest

from flaskapp import create_app


class TestCaseManagementTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        config_override = {"TESTING": True}
        os.environ["DATABASE_FILENAME"] = "testdb.db"
        self.app = create_app(config_override)
        self.client = self.app.test_client

        self.new_test_case = {
            "name": "New Test Case",
            "description": "New Test Case Description",
        }

        self.new_execution = {
            "asset_id": "1",
            "test_case_id": "1",
            "status": True,
            "details": "Success",
        }

    def tearDown(self):
        """Executed after each test"""
        pass

    def test_retrieve_tests(self):
        """Test retrieve tests"""
        res = self.client().get("/tests")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["test_cases"])

    def test_405_using_wrong_method_to_retrieve_tests(self):
        """Test 405 using wrong method to retrieve tests"""
        res = self.client().patch("/tests")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"])

    def test_create_new_test(self):
        """test create new test"""
        res = self.client().post("/tests", json=self.new_test_case)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_400_create_new_test_without_name(self):
        """test create new test without providing name"""
        res = self.client().post("/tests", json={"testing": "xxx"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"])

    def test_405_creation_not_allowed(self):
        """test 405 creation not allowed"""
        res = self.client().post("/tests/45", json=self.new_test_case)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"])

    def test_get_specific_test(self):
        """Test get specific test with id"""
        res = self.client().get("/tests/1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["test_case"]))

    def test_get_nonexistent_test(self):
        """Test get non existent test"""
        res = self.client().get("/tests/10000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"])

    def test_update_test(self):
        """Test update test"""
        res = self.client().patch("/tests/1", json={"name": "Updated Test Case"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["test_case"])

    def test_update_test_without_name(self):
        """Test update test without providing name"""
        res = self.client().patch("/tests/1", json={"testing": "Updated Test Case"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"])

    def test_delete_test_case(self):
        """Test delete test case"""
        res = self.client().delete("/tests/3")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted_test_case_id"], 5)
        self.assertTrue(data["total_test_cases"])

    def test_404_delete_nonexistent_test(self):
        """test 404 delete nonexistent test"""
        res = self.client().delete("/tests/10000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"])

    def test_get_execution_results(self):
        """Test get execution results"""
        res = self.client().get("/executions/1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["executions"])
        self.assertTrue(data["asset"])
        self.assertTrue(data["total_executions"])

    def test_add_execution_results(self):
        """Test add execution result"""
        res = self.client().post("/executions", json=self.new_execution)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["execution"])
        self.assertTrue(data["total_executions"])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
