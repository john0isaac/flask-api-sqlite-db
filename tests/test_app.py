import pytest


@pytest.fixture
def client(app_with_db):
    return app_with_db.test_client()


def test_index(client):
    """Test index page"""
    response = client.get("/")
    body = response.get_json()

    assert response.status_code == 200
    assert body["success"] is True
    assert body["message"] == "Welcome to the test case management API"


def test_retrieve_tests(client):
    """Test retrieve tests"""
    response = client.get("/tests")
    body = response.get_json()

    assert response.status_code == 200
    assert body["success"] is True
    assert body["test_cases"]


def test_405_using_wrong_method_to_retrieve_tests(client):
    """Test 405 using wrong method to retrieve tests"""
    response = client.patch("/tests")
    body = response.get_json()

    assert response.status_code == 405
    assert body["success"] is False
    assert body["message"]


def test_create_new_test(client):
    """test create new test"""
    response = client.post(
        "/tests",
        json={
            "name": "New Test Case",
            "description": "New Test Case Description",
        },
    )
    body = response.get_json()

    assert response.status_code == 200
    assert body["success"] is True


def test_400_create_new_test_without_name(client):
    """test create new test without providing name"""
    response = client.post("/tests", json={"testing": "xxx"})
    body = response.get_json()

    assert response.status_code == 400
    assert body["success"] is False
    assert body["message"]


def test_405_creation_not_allowed(client):
    """test 405 creation not allowed"""
    response = client.post(
        "/tests/45",
        json={
            "name": "New Test Case",
            "description": "New Test Case Description",
        },
    )
    body = response.get_json()

    assert response.status_code == 405
    assert body["success"] is False
    assert body["message"]


def test_get_specific_test(client):
    """Test get specific test with id"""
    response = client.get("/tests/1")
    body = response.get_json()

    assert response.status_code == 200
    assert body["success"] is True
    assert len(body["test_case"])


def test_get_nonexistent_test(client):
    """Test get non existent test"""
    response = client.get("/tests/10000")
    body = response.get_json()

    assert response.status_code == 404
    assert body["success"] is False
    assert body["message"]


def test_update_test(client):
    """Test update test"""
    response = client.patch("/tests/1", json={"name": "Updated Test Case"})
    body = response.get_json()

    assert response.status_code == 200
    assert body["success"] is True
    assert body["test_case"]


def test_update_test_without_name(client):
    """Test update test without providing name"""
    response = client.patch("/tests/1", json={"testing": "Updated Test Case"})
    body = response.get_json()

    assert response.status_code == 400
    assert body["success"] is False
    assert body["message"]


def test_404_delete_nonexistent_test(client):
    """test 404 delete nonexistent test"""
    response = client.delete("/tests/10000")
    body = response.get_json()

    assert response.status_code == 404
    assert body["success"] is False
    assert body["message"]


def test_get_execution_results(client):
    """Test get execution results"""
    response = client.get("/executions/1")
    body = response.get_json()

    assert response.status_code == 200
    assert body["success"] is True
    assert body["executions"]
    assert body["asset"]
    assert body["total_executions"]


def test_add_execution_results(client):
    """Test add execution result"""
    response = client.post(
        "/executions",
        json={
            "asset_id": "1",
            "test_case_id": "1",
            "status": True,
            "details": "Success",
        },
    )
    body = response.get_json()

    assert response.status_code == 200
    assert body["success"] is True
    assert body["execution"]
    assert body["total_executions"]
