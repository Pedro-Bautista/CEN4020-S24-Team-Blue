# Authentication Controller
# Handles sign in and sign up requests

from flask import request, jsonify
import incollege.services.AuthService as AuthService


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

    @app.route('/job_post', methods=['POST']) 
    def handle_job_post():
        data = request.get_json()
        title = data.get('title')
        desc = data.get('desc')
        employer = data.get('employer')
        location = data.get('location')
        salary = data.get('salary')
            
        AuthService.job_post(title, desc, employer, location, salary)
    
        return jsonify({'message': 'Job posted successfully'}), 201
        
    @app.route('/user_search', methods=['POST']) 
    def handle_user_search():
        data = request.get_json()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        
        return jsonify({'message': AuthService.find_user_name(first_name, last_name)}), 200