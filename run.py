#!/usr/bin/env python3
"""
Standalone run script for ReWear application
Can be used instead of Gunicorn for development
"""

import os
from dotenv import load_dotenv  # 👈 1. Import dotenv
load_dotenv() 
from app import app
import populate_database

if __name__ == '__main__':
    # Set default environment variables for development
    if not os.environ.get('DATABASE_URL'):
        os.environ['DATABASE_URL'] = 'sqlite:///rewear.db'
    
    if not os.environ.get('SESSION_SECRET'):
        os.environ['SESSION_SECRET'] = 'dev-secret-key-change-in-production'
    
    # Run the app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )