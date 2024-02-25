import json
import os

import pytest
from flask import Flask

from incollege.config import Config
from incollege.controllers.ControllerAdvice import configure_controller_advice
from incollege.controllers.JobController import configure_job_routes
from incollege.repositories.DBConnector import create_tables


@pytest.fixture(scope='module')
def test_client():
    test_app = Flask(__name__)
    test_app.config['TESTING'] = True
    configure_job_routes(test_app)
    configure_controller_advice(test_app)

    print('Attempting to reset database...')
    try:
        os.remove(Config.DATABASE_NAME)
        print('Successfully deleted existing test database.')
    except FileNotFoundError:
        print('Test database not found. Creating...')
    create_tables()
    print('Created new test database.')

    with test_app.test_client() as test_client:
        with test_app.app_context():
            yield test_client