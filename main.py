# CEN4020 Team Blue main file
# Members - Pedro Bautista, Austin Holmes, Mirshokhid Okilbekov, Ruben Romero, Ye Zhang

from flask import Flask
from flask_cors import CORS

import incollege.repositories.DBConnector as DB
from incollege.controllers.AuthController import configure_auth_routes
from incollege.controllers.ControllerAdvice import configure_controller_advice

# Configure endpoints
app = Flask(__name__)
CORS(app)
configure_auth_routes(app)

# Controller Error Handler
configure_controller_advice(app)

# Initialize database
DB.create_tables()

if __name__ == '__main__':
    app.run(debug=True)
