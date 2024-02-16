# Authentication Controller
# Handles sign in and sign up requests

from flask import request, jsonify
from incollege.services import JobService


def configure_job_routes(app):
    @app.route('/job_post', methods=['POST'])
    def handle_job_post():
        data = request.get_json()
        title = data.get('title')
        desc = data.get('desc')
        employer = data.get('employer')
        location = data.get('location')
        salary = data.get('salary')

        JobService.post_job(title, desc, employer, location, salary)

        return jsonify({'message': 'Job posted successfully'}), 201
