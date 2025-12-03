"""
Database configuration and setup
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import os

# Initialize SQLAlchemy
db = SQLAlchemy()
Base = declarative_base()

# Database configuration
DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ecommerce.db')
SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'

def init_db(app):
    """Initialize database with Flask app"""
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        # Import models to register them with SQLAlchemy
        from ecommerce.models import db_models
        db.create_all()
        print(f"✓ Database initialized at: {DATABASE_PATH}")

