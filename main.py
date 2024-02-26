# CEN4020 Team Blue main file
# Members - Pedro Bautista, Austin Holmes, Mirshokhid Okilbekov, Ruben Romero, Ye Zhang

from flask import Flask
from flask_cors import CORS

import incollege.repositories.DBConnector as DB
from incollege.controllers.AuthController import configure_auth_routes
from incollege.controllers.ControllerAdvice import configure_controller_advice
from incollege.controllers.JobController import configure_job_routes
from incollege.controllers.UserController import configure_user_routes
from incollege.controllers.ConnectionsController import configure_connection_routes

# Configure endpoints
app = Flask(__name__)
CORS(app)
configure_auth_routes(app)
configure_job_routes(app)
configure_user_routes(app)
configure_connection_routes(app)


# Controller Error Handler
configure_controller_advice(app)

# Initialize database
DB.create_tables()

if __name__ == '__main__':
    app.run(debug=True)
