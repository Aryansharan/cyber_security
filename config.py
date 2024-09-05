import os
from sqlalchemy.engine.url import URL

# Database configuration
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///ip_location.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
