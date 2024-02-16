# Authentication Controller
# Handles sign in and sign up requests

from flask import request, jsonify
import incollege.services.AuthService as AuthService
import incollege.services.UserService


def configure_auth_routes(app):
    @app.route('/')
    def index():
        return 'Welcome to InCollege!'

    @app.route('/login', methods=['POST'])
    def handle_login():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        return jsonify({'token': AuthService.login(username, password)})

    @app.route('/signup', methods=['POST'])
    def handle_signup():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        return jsonify({'token': AuthService.signup(username, password, first_name, last_name)}), 201
