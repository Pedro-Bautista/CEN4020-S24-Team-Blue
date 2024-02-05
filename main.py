# CEN4020 Team Blue main file
# Members-Pedro Bautista, Austin Holmes, Mirshokhid Okilbekov, Ruben Romero, Ye Zhang

import incollege.repositories.DBConnector as DB
import incollege.controllers.AuthController as Auth

# Initialize database
DB.create_tables()


print(Auth.login('austin', 'sp3ci@L8'))


# Close database connection
DB.close_connection()
