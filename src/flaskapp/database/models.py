"""
Models for MySQL

"""

from datetime import datetime

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()

"""
    setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config.get("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()


"""
    db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
"""


def db_drop_and_create_all(app):
    with app.app_context():
        db.drop_all()
        db.create_all()


# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#


class TestCase(db.Model):
    __tablename__ = "test_case"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    executions: Mapped[list["Execution"]] = relationship("Execution", back_populates="test_case")

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {"id": self.id, "name": self.name, "description": self.description}


class Asset(db.Model):
    __tablename__ = "asset"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    executions: Mapped[list["Execution"]] = relationship("Execution", back_populates="asset")

    def __init__(self, name):
        self.name = name

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {"id": self.id, "name": self.name}


class Execution(db.Model):
    __tablename__ = "execution"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    test_case_id: Mapped[int] = mapped_column(ForeignKey("test_case.id"))
    test_case: Mapped["TestCase"] = relationship("TestCase", back_populates="executions")
    asset_id: Mapped[int] = mapped_column(ForeignKey("asset.id"))
    asset: Mapped["Asset"] = relationship("Asset", back_populates="executions")
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False)
    details: Mapped[str] = mapped_column(String(500))

    def __init__(self, test_case_id, asset_id, status, details):
        self.test_case_id = test_case_id
        self.asset_id = asset_id
        self.status = status
        self.details = details

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "test_case_id": self.test_case_id,
            "asset_id": self.asset_id,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "status": self.status,
            "details": self.details,
        }
