from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
import sqlite3
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    preferences = data.get('preferences', '')
    language = data.get('language', 'en')

    # Input validation
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Check if username exists
    conn = sqlite3.connect('database/data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    if cursor.fetchone():
        return jsonify({"error": "Username already exists"}), 400

    cursor.execute('INSERT INTO users (username, password, preferences, language) VALUES (?, ?, ?, ?)',
                   (username, password, preferences, language))
    conn.commit()
    conn.close()

    return jsonify({"message": "User registered successfully!"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    conn = sqlite3.connect('database/data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.check_password_hash(user[2], password):
        # Create access token with expiration time
        token = create_access_token(identity={"id": user[0], "username": user[1]}, expires_delta=timedelta(hours=24))
        return jsonify({"token": token}), 200
    return jsonify({"message": "Invalid credentials!"}), 401
