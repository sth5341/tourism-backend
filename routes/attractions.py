from flask import Blueprint, request, jsonify
import sqlite3

# Initialize Blueprint
attractions_bp = Blueprint('attractions', __name__)

# Database Path
DB_PATH = 'database/data.db'

# Helper function to get DB connection
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Allows access to columns by name
    return conn

# Route: Get All Attractions
@attractions_bp.route('/', methods=['GET'])
def get_all_attractions():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM attractions')
        attractions = cursor.fetchall()
        conn.close()

        # Format the results into JSON
        result = [
            {
                "id": row[0],
                "name": row[1],
                "type": row[2],
                "location": {"latitude": row[3], "longitude": row[4]},
                "rating": row[5],
                "price": row[6],
                "opening_hours": row[7],
            }
            for row in attractions
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route: Add a New Attraction
@attractions_bp.route('/', methods=['POST'])
def add_attraction():
    data = request.json
    try:
        # Input Validation
        if not all(key in data for key in ['name', 'type', 'location', 'rating', 'price', 'opening_hours']):
            return jsonify({"error": "Missing required fields"}), 400

        if not isinstance(data['rating'], (int, float)) or not (1 <= data['rating'] <= 5):
            return jsonify({"error": "Invalid rating, must be between 1 and 5"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO attractions (name, type, latitude, longitude, rating, price, opening_hours)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                data['name'],
                data['type'],
                data['location']['latitude'],  # Assuming location is passed as a dict
                data['location']['longitude'],
                data['rating'],
                data['price'],
                data['opening_hours'],
            ),
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Attraction added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route: Search for Attractions
@attractions_bp.route('/search', methods=['GET'])
def search_attractions():
    attraction_type = request.args.get('type')
    location = request.args.get('location')
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = 'SELECT * FROM attractions WHERE 1=1'
        params = []

        if attraction_type:
            query += ' AND type = ?'
            params.append(attraction_type)

        if location:
            query += ' AND location = ?'
            params.append(location)

        cursor.execute(query, params)
        attractions = cursor.fetchall()
        conn.close()

        # Format results into JSON
        result = [
            {
                "id": row[0],
                "name": row[1],
                "type": row[2],
                "location": {"latitude": row[3], "longitude": row[4]},
                "rating": row[5],
                "price": row[6],
                "opening_hours": row[7],
            }
            for row in attractions
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
