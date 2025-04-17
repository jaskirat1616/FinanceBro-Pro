import os
from app import create_app
from config import DefaultConfig

app = create_app(DefaultConfig)

if __name__ == '__main__':
    # Use development configuration for local running
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() in ['true', '1', 't']
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 3000))
    
    app.run(debug=debug_mode, host=host, port=port)