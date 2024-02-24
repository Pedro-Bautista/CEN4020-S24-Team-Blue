import json
from unittest import mock
import pytest
from flask import Flask

from incollege.controllers.AuthController import configure_auth_routes
from incollege.exceptions.AuthException import AuthException


@pytest.fixture(scope='module')
def test_client():
    test_app = Flask(__name__)
    test_app.config['TESTING'] = True
    configure_auth_routes(test_app)

    with test_app.test_client() as test_client:
        with test_app.app_context():
            yield test_client