import multiprocessing
import os

# Gunicorn configuration for production deployment

# Set environment variables
os.environ.setdefault('FLASK_ENV', 'production')

# Bind to host and port
bind = os.getenv('GUNICORN_BIND', '0.0.0.0:5000')

# Number of worker processes
workers = int(os.getenv('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))

# Worker class - choose an appropriate one based on the workload
worker_class = os.getenv('GUNICORN_WORKER_CLASS', 'gevent')

# Maximum requests a worker will process before restarting
max_requests = int(os.getenv('GUNICORN_MAX_REQUESTS', 1000))
max_requests_jitter = int(os.getenv('GUNICORN_MAX_REQUESTS_JITTER', 50))

# Timeout for worker processes (in seconds)
timeout = int(os.getenv('GUNICORN_TIMEOUT', 30))

# Whether to enable keepalive (seconds)
keepalive = int(os.getenv('GUNICORN_KEEPALIVE', 2))

# Access log - file path or "-" for stdout
accesslog = os.getenv('GUNICORN_ACCESS_LOG', '-')

# Error log - file path or "-" for stderr
errorlog = os.getenv('GUNICORN_ERROR_LOG', '-')

# Logging level
loglevel = os.getenv('GUNICORN_LOG_LEVEL', 'info')

# Process name (showing up in process listings)
proc_name = 'financebro_pro'

# Preload the application to reduce memory usage
preload_app = os.getenv('GUNICORN_PRELOAD', 'true').lower() in ['true', '1', 't']

# SSL configuration (uncomment for HTTPS)
# keyfile = '/path/to/keyfile'
# certfile = '/path/to/certfile'

# When running behind a proxy like Nginx
# proxy_protocol = True
# proxy_allow_ips = '*'

# Define post-fork and pre-fork hooks if needed
def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def pre_fork(server, worker):
    server.log.info("Pre-forking worker")

def on_starting(server):
    server.log.info("Server is starting")

def on_exit(server):
    server.log.info("Server is shutting down") 