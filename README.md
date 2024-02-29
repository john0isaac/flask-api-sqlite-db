# flask-api-sqlite-db
API for Managing test cases and their execution results across multiple test assets, with data stored in a SQLite database.

## Running the app

To run the Flask application, follow these steps:

1. **Download the project starter code locally**

    ```bash
    git clone https://github.com/john0isaac/flask-api-sqlite-db.git
    cd flask-api-sqlite-db
    ```

1. **Install, initialize and activate a virtualenv using:**

    ```bash
    pip install virtualenv
    python -m virtualenv venv
    source venv/bin/activate
    ```

    >**Note** - In Windows, the `venv` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:

    ```bash
    source venv\Scripts\activate
    ```

1. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

1. **Execute the following command in your terminal to start the flask app**

    ```bash
    export DATABASE_FILENAME=testdb.db
    export FLASK_APP=src.app
    export FLASK_ENV=development
    flask run --reload
    ```
### Run the tests

1. **Inside your virtual environment, execute the following command to run the tests**

    ```bash
    python flask_test.py
    ```

## API Documentation

### Error handling

Invoking any of the following errors will return a JSON object in this format:

```JSON
{
  "success": False,
  "error": 400,
  "message": "bad request"
}
```

The API will return these error types when the request fails:

- 400: Bad Request
- 405: Method Not Allowed
- 422: Not Processable
- 404: Resource Not Found

### Endpoints

**GET /tests**

- Sample

```JSON
{
    "success": true,
    "test_cases": [
        {
            "description": "First Test Description",
            "id": 1,
            "name": "Updated Test Case"
        },
        {
            "description": null,
            "id": 2,
            "name": "Second Test"
        }
    ],
    "total_test_cases": 5
}
```

**POST /tests**

- Sample

```JSON
{
    "success": true,
    "test_case": {
        "description": "Fifth Test Case Description",
        "id": 6,
        "name": "Fifth Test Case"
    },
    "total_test_cases": 6
}
```

**GET /tests/{test.id}**

- Sample

```JSON
{
    "success": true,
    "test_case": {
        "description": "Fifth Test Case Description",
        "id": 6,
        "name": "Fifth Test Case"
    }
}
```

**PATCH /tests/{test.id}**

- Sample

```JSON
{
    "success": true,
    "test_case": {
        "description": "Sixth Test Case Description",
        "id": 6,
        "name": "Sixth Test Case"
    },
    "total_test_cases": 6
}
```

**DELETE /tests**

- Sample

```JSON
{
    "deleted_test_case_id": 6,
    "success": true,
    "total_test_cases": 5
}
```

**GET /executions**

- Sample

```JSON
{
    "asset": {
        "id": 2,
        "name": "Second Asset"
    },
    "executions": [
        {
            "details": "Success",
            "execution_date": "Sat, 02 Mar 2024 17:35:30 GMT",
            "id": 4,
            "status": true,
            "test_case": {
                "id": 1,
                "name": "Updated Test Case"
            }
        },
        {
            "details": "Success",
            "execution_date": "Sun, 03 Mar 2024 18:35:30 GMT",
            "id": 5,
            "status": true,
            "test_case": {
                "id": 3,
                "name": "Third Test"
            }
        }
    ],
    "success": true,
    "total_executions": 2
}
```

**POST /executions**

- Sample

```JSON
{
    "execution": {
        "asset_id": 1,
        "details": "Sucess",
        "id": 10,
        "status": true,
        "test_case_id": 1,
        "timestamp": "2024-02-29 09:36:57"
    },
    "success": true,
    "total_executions": 10
}
```


