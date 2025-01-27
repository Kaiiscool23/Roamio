from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="nift2017",
    database="appasholidays"
)

# Login Endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    cursor = db.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()

    if user:
        return jsonify({'success': True, 'message': 'Login successful', 'user_id': user[0]})
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

if __name__ == "__main__":
    app.run(debug=True)
