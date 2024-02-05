# CEN4020 Team Blue main file
# Members-Pedro Bautista, Austin Holmes, Mirshokhid Okilbekov, Ruben Romero, Ye Zhang

import incollege.repositories.DBConnector as DB
import incollege.controllers.AuthController as Auth

# Initialize database
DB.create_tables()


print(Auth.signup('austin', '1234'))
print(Auth.signup('bob', '4321'))
print(Auth.signup('alice', '4321'))
print(Auth.signup('jane', '4321'))
print(Auth.signup('clifford', '4321'))
print(Auth.signup('sina', '1234'))


# Close database connection
DB.close_connection()
