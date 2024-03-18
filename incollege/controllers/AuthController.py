# Authentication Controller
# Handles sign in and sign up requests

from flask import request, jsonify, Flask
import incollege.services.AuthService as AuthService


def configure_auth_routes(app: Flask):
    """Invoked to bind routes pertaining to this controller class.

    Args:
        app: The currently running Flask app instance.
    """
    @app.route('/')
    def index():
        """Default HTML route.

        Returns:
            str: Basic placeholder welcome message.
        """
        return 'Welcome to InCollege!'

    @app.route('/login', methods=['POST'])
    def handle_login():
        """Route for login process. Expects a username and password.

        Returns:
            Response: A session token in the form of an encoded :obj:`AuthJWT`.
        """
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        return jsonify({'token': AuthService.login(username, password)})

    @app.route('/signup', methods=['POST'])
    def handle_signup():
        """Route for signup process. Expects a username and password, along with a first and last name.

        Returns:
            Response: A session token in the form of an encoded :obj:`AuthJWT` with status 201.
        """
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        return jsonify({'token': AuthService.signup(username, password, first_name, last_name)}), 201
