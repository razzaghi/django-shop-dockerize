"""gunicorn WSGI server configuration."""
from multiprocessing import cpu_count
from os import environ


def max_workers():    
    return cpu_count() * 5


bind = '0.0.0.0:' + environ.get('PORT', '8000')
max_requests = 1000
# worker_class = 'gevent'
workers = 2
timeout = 36000
errorlog = '-'
loglevel = 'debug'
accesslog = '-'
