"""
Configuration settings for the Code Diary application
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_very_secret_and_random_key_for_flash_messages')
    DEBUG = False
    TESTING = False
    
    # Database
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    # Ensure the instance folder exists for the SQLite database
    instance_path = os.path.join(basedir, 'instance')
    os.makedirs(instance_path, exist_ok=True)
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(instance_path, 'code_diary.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Google AI
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Select config based on environment
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
