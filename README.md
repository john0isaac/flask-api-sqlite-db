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
