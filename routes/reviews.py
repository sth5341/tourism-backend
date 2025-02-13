from flask import Blueprint, jsonify, request
import sqlite3

# Initialize Blueprint
reviews_bp = Blueprint('reviews', __name__)

# Database Path
DB_PATH = 'database/data.db'

# Helper function for DB connection
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Allows access to columns by name
    return conn

@reviews_bp.route('/', methods=['GET'])
def get_reviews():
    """
    Fetch all reviews.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM reviews')
        reviews = cursor.fetchall()
        conn.close()

        # Format the results into JSON
        result = [
            {
                "id": row[0],
                "attraction_id": row[1],
                "user_id": row[2],
                "review": row[3],
                "rating": row[4],
            }
            for row in reviews
        ]
        return jsonify(result), 200

    except sqlite3.Error as db_error:
        return jsonify({"error": f"Database error: {str(db_error)}"}), 500

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@reviews_bp.route('/', methods=['POST'])
def add_review():
    """
    Add a new review.
    """
    data = request.json
    try:
        # Input validation
        if not all(key in data for key in ['attraction_id', 'user_id', 'review', 'rating']):
            return jsonify({"error": "Missing required fields"}), 400

        if not (1 <= data['rating'] <= 5):
            return jsonify({"error": "Rating must be between 1 and 5"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO reviews (attraction_id, user_id, review, rating) VALUES (?, ?, ?, ?)',
            (
                data['attraction_id'],
                data['user_id'],
                data['review'],
                data['rating'],
            )
        )
        conn.commit()
        conn.close()

        return jsonify({"message": "Review added successfully!"}), 201

    except sqlite3.Error as db_error:
        return jsonify({"error": f"Database error: {str(db_error)}"}), 500

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
