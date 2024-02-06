# CEN4020 Team Blue main file
# Members-Pedro Bautista, Austin Holmes, Mirshokhid Okilbekov, Ruben Romero, Ye Zhang

from flask import Flask, request, jsonify
import incollege.repositories.DBConnector as DB
import incollege.controllers.AuthController as Auth

app = Flask(__name__)

# Initialize database
DB.create_tables()

@app.route('/')
def index():
	return 'Welcome to InCollege!'

@app.route('/login', methods=['POST'])
def handle_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    result = Auth.login(username, password)

    if result[0]:
        result = {'success': True, 'token': result[1]}
    else:
        result = {'success': False, 'error': result[1]}

    return jsonify(result)

@app.route('/signup', methods=['POST'])
def handle_signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    result = Auth.signup(username, password)

    if result[0]:
        result = {'success': True, 'token': result[1]}
    else:
        result = {'success': False, 'error': result[1]}

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)


# Close database connection
DB.close_connection()
