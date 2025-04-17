from flask import Flask, g
from flask_caching import Cache
from config import Config
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import os

# Initialize extensions
cache = Cache()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    cache.init_app(app)
    
    # Setup logging for production
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/financebro.log', 
                                          maxBytes=10240, 
                                          backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('FinanceBro Pro startup')
    
    # Make 'now' available to all templates
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}
    
    # Register blueprints
    from app.routes import bp
    app.register_blueprint(bp)
    
    # Register error handlers
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    
    return app