import pytest
from flask import Flask
from incollege.config import Config
from incollege.controllers.ConnectionsController import configure_connection_routes
from incollege.controllers.ControllerAdvice import configure_controller_advice
from incollege.repositories.DBConnector import create_tables
import os

@pytest.fixture(scope='module')
def connections_test_client():
    app = Flask(__name__)
    app.config.from_object(Config)
    configure_connection_routes(app)
    configure_controller_advice(app)

    if os.path.exists(Config.DATABASE_NAME):
        os.remove(Config.DATABASE_NAME)
    create_tables()

    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client
