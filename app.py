import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager


app = Flask(__name__)

# Configure CORS for specific domains
CORS(app, resources={r"/api/*": {"origins": os.getenv('WECHAT_DOMAIN', 'https://tourism-backend-z2z4.onrender.com')}})

# Configure JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')  # Use environment variable for security
jwt = JWTManager(app)

# Configure debug mode
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False') == 'True'

# Import Routes
from routes.auth import auth_bp
from routes.attractions import attractions_bp
from routes.recommendations import recommendations_bp
from routes.reviews import reviews_bp

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(attractions_bp, url_prefix='/api/attractions')
app.register_blueprint(recommendations_bp, url_prefix='/api/recommendations')
app.register_blueprint(reviews_bp, url_prefix='/api/reviews')

if __name__ == '__main__':
    app.run(debug=True)
