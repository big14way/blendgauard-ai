#!/usr/bin/env python3
"""
BlendGuard Backend API
Main Flask application with notification endpoints
"""
import os
import logging
from flask import Flask
from flask_cors import CORS
from api.notify import bp as notify_bp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    CORS(app)  # Enable CORS for frontend requests
    
    # Register blueprints
    app.register_blueprint(notify_bp, url_prefix='/api')
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return {'status': 'healthy', 'service': 'blendguard-backend'}
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    # Use port 5001 to avoid conflict with macOS AirPlay Receiver on port 5000
    port = int(os.environ.get('PORT', 5001))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_DEBUG', 'true').lower() == 'true'
    
    logger.info(f"Starting BlendGuard Backend API on {host}:{port}")
    app.run(host=host, port=port, debug=debug) 