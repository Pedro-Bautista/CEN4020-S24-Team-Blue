# CEN4020 Team Blue main file
# Members-Pedro Bautista, Austin Holmes, Mirshokhid Okilbekov, Ruben Romero, Ye Zhang

import incollege.repositories.DBConnector as DB
import incollege.controllers.AuthController as Auth

# Initialize database
DB.create_tables()


print(Auth.signup('austin', '1234'))
print(Auth.login('bob', '4321'))


# Close database connection
DB.close_connection()
