import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration class"""
    # Security settings
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24).hex())
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.getenv('WTF_CSRF_SECRET_KEY', os.urandom(24).hex())
    
    # API Keys
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    ALPACA_API_KEY = os.getenv('ALPACA_API_KEY', '')
    ALPACA_SECRET_KEY = os.getenv('ALPACA_SECRET_KEY', '')
    
    # Cache configuration
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'SimpleCache')
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', 300))
    CACHE_THRESHOLD = 500  # Maximum number of items the cache will store
    
    # App specific settings
    APP_NAME = 'FinanceBro Pro'
    STOCK_DATA_CACHE_TIMEOUT = int(os.getenv('STOCK_DATA_CACHE_TIMEOUT', 60))  # 1 minute
    COMPANY_INFO_CACHE_TIMEOUT = int(os.getenv('COMPANY_INFO_CACHE_TIMEOUT', 86400))  # 24 hours
    
    # Rate limiting
    RATELIMIT_DEFAULT = os.getenv('RATELIMIT_DEFAULT', '200 per day, 50 per hour')
    RATELIMIT_STORAGE_URL = os.getenv('RATELIMIT_STORAGE_URL', 'memory://')
    
    # Logging
    LOG_TO_STDOUT = os.getenv('LOG_TO_STDOUT', 'false').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    
class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = False
    TESTING = True
    WTF_CSRF_ENABLED = False
    CACHE_TYPE = 'NullCache'
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Use more robust cache in production if Redis is available
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'SimpleCache')
    if CACHE_TYPE == 'RedisCache':
        CACHE_REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
        CACHE_REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
        CACHE_REDIS_DB = int(os.getenv('REDIS_DB', 0))
        CACHE_REDIS_URL = os.getenv('REDIS_URL', '')
    
    # Enable SSL in production
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

# Select configuration based on environment
config_classes = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# Default to development configuration
config_name = os.getenv('FLASK_ENV', 'default')
DefaultConfig = config_classes[config_name]