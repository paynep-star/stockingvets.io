import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///stockingvets.db')
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}