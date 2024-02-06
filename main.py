# CEN4020 Team Blue main file
# Members-Pedro Bautista, Austin Holmes, Mirshokhid Okilbekov, Ruben Romero, Ye Zhang

from flask import Flask, jsonify
from werkzeug.exceptions import BadRequest

import incollege.repositories.DBConnector as DB
from incollege.controllers.AuthController import configure_auth_routes
from incollege.exceptions import EndpointException

# Configure endpoints
app = Flask(__name__)
configure_auth_routes(app)


# Global exception handler
@app.errorhandler(Exception)
def handle_exception(error):
    code = 503
    if isinstance(error, EndpointException.EndpointException):
        code = error.http_code
    elif isinstance(error, BadRequest):
        code = 400

    response = {
        'error': {
            'code': code,
            'description': str(error)
        }
    }

    return jsonify(response), code


# Initialize database
DB.create_tables()

if __name__ == '__main__':
    app.run(debug=True)
