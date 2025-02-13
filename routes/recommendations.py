from flask import Blueprint, jsonify, request
import sqlite3
from math import radians, sin, cos, sqrt, atan2

# Initialize Blueprint
recommendations_bp = Blueprint('recommendations', __name__)

# Database Path
DB_PATH = 'database/data.db'

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance between two points on the Earth's surface"""
    R = 6371  # Radius of the Earth in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c  # Returns distance in kilometers

@recommendations_bp.route('/', methods=['GET'])
def get_recommendations():
    """
    Fetch all attractions as recommendations.
    Optionally filter by user preferences and/or location (latitude, longitude).
    """
    try:
        user_lat = float(request.args.get('latitude'))
        user_lon = float(request.args.get('longitude'))
        user_preferences = request.args.get('preferences')  # Optional: filter by attraction type

        # Connect to the database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Query attractions based on preferences (if provided)
        if user_preferences:
            cursor.execute('SELECT * FROM attractions WHERE type = ?', (user_preferences,))
        else:
            cursor.execute('SELECT * FROM attractions')
        
        attractions = cursor.fetchall()
        conn.close()

        # Calculate distance for each attraction
        result = []
        for row in attractions:
            attraction_lat = row[3]  # Latitude
            attraction_lon = row[4]  # Longitude
            distance = haversine(user_lat, user_lon, attraction_lat, attraction_lon)
            result.append({
                "id": row[0],
                "name": row[1],
                "type": row[2],
                "location": {"latitude": row[3], "longitude": row[4]},
                "rating": row[5],
                "price": row[6],
                "opening_hours": row[7],
                "distance": distance
            })

        # Sort by distance
        result.sort(key=lambda x: x['distance'])

        return jsonify(result), 200

    except (TypeError, ValueError):
        return jsonify({"error": "Invalid latitude or longitude"}), 400

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
