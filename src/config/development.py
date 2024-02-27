import os
from pathlib import Path

DEBUG = True

database_filename = os.environ["DATABASE_FILENAME"]
BASE_DIR = Path(__file__).resolve().parent.parent
database_dir = os.path.join(BASE_DIR, "database")
DATABASE_URI = f"sqlite:///{os.path.join(database_dir, database_filename)}"
